"""Gateway-facing orchestration for RAG requests and telemetry.

The FastAPI layer delegates here so health checks, source metadata extraction,
request IDs, provider metadata, and privacy-preserving MLflow logging are tested
independently from HTTP routing.
"""

from __future__ import annotations

import os
import time
import uuid
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.rag import config, mlflow_tracker
from src.rag.logger import get_logger

logger = get_logger(__name__)

DEFAULT_GATEWAY_PROVIDER = "vllm"
DEFAULT_VECTOR_STORE = "qdrant"
SOURCE_SNIPPET_CHARS = 280


@dataclass
class RAGServiceResult:
    """Completed non-streaming RAG answer plus public metadata."""

    request_id: str
    answer: str
    sources: list[dict[str, Any]]
    metadata: dict[str, Any]


@dataclass
class RAGServiceStream:
    """Streaming RAG response state used to finalize telemetry after SSE output."""

    request_id: str
    chunks: Iterable[str]
    sources: list[dict[str, Any]]
    metadata: dict[str, Any]
    started_at: float
    question: str = field(repr=False)


class RAGService:
    """Orchestrates chain invocation, source extraction, health, and logging."""

    def __init__(
        self,
        *,
        chain_factory: Optional[Callable[[], Any]] = None,
        provider_name: str = DEFAULT_GATEWAY_PROVIDER,
        vector_store_type: str = DEFAULT_VECTOR_STORE,
    ) -> None:
        self._chain_factory = chain_factory or _default_rag_chain_factory
        self._chain_instance: Any = None
        self.provider_name = os.environ.get("RAG_GATEWAY_LLM_PROVIDER", provider_name)
        self.vector_store_type = os.environ.get("RAG_GATEWAY_VECTOR_STORE", vector_store_type)

    def answer(self, question: str) -> RAGServiceResult:
        """Run a non-streaming RAG request and log sanitized request metadata."""

        request_id = self.new_request_id()
        started_at = time.perf_counter()
        result = self._get_chain().invoke(question)
        answer = normalize_rag_answer(result)
        sources = extract_rag_sources(result)
        metadata = self._metadata(
            question=question,
            request_id=request_id,
            sources=sources,
            started_at=started_at,
        )
        self.log_request(metadata)
        return RAGServiceResult(
            request_id=request_id,
            answer=answer,
            sources=sources,
            metadata=metadata,
        )

    def start_stream(self, question: str) -> RAGServiceStream:
        """Start a streaming response, falling back to one chunk when needed."""

        request_id = self.new_request_id()
        started_at = time.perf_counter()
        chain = self._get_chain()
        stream_answer = getattr(chain, "stream_answer", None)

        if callable(stream_answer):
            stream_result = stream_answer(question)
            context = (
                list(stream_result.get("context") or [])
                if isinstance(stream_result, dict)
                else []
            )
            chunks = (
                stream_result.get("chunks") or []
                if isinstance(stream_result, dict)
                else stream_result
            )
            sources = extract_rag_sources({"context": context})
        else:
            result = chain.invoke(question)
            answer = normalize_rag_answer(result)
            chunks = [answer] if answer else []
            sources = extract_rag_sources(result)

        return RAGServiceStream(
            request_id=request_id,
            chunks=chunks,
            sources=sources,
            metadata=self._base_metadata(
                question=question,
                request_id=request_id,
                sources=sources,
            ),
            started_at=started_at,
            question=question,
        )

    def finalize_stream(self, stream: RAGServiceStream, answer: str) -> dict[str, Any]:
        """Record successful stream completion and return public metadata."""

        metadata = dict(stream.metadata)
        metadata["latency_ms"] = _elapsed_ms(stream.started_at)
        metadata["completion_hash"] = mlflow_tracker.hash_text(answer)
        stream.metadata = metadata
        self.log_request(metadata)
        return metadata

    def fail_stream(self, stream: RAGServiceStream, exc: Exception) -> dict[str, Any]:
        """Record stream failure without persisting raw question or answer text."""

        metadata = dict(stream.metadata)
        metadata["latency_ms"] = _elapsed_ms(stream.started_at)
        metadata["error_type"] = exc.__class__.__name__
        stream.metadata = metadata
        self.log_request(metadata, failed=True)
        return metadata

    def health(self) -> dict[str, Any]:
        """Return gateway health without initializing the expensive RAG chain."""

        backend = self.provider_metadata()
        provider_health = self.provider_health()
        return {
            "status": "ok",
            "service": "rag-gateway",
            "backend": {
                **backend,
                "provider_health": provider_health,
            },
        }

    def provider_metadata(self) -> dict[str, Any]:
        """Expose safe provider/vector settings for health and model metadata."""

        provider_kwargs = config.provider_kwargs(self.provider_name)
        return {
            "backing_provider": self.provider_name,
            "backing_model": provider_kwargs.get("model"),
            "backing_base_url": provider_kwargs.get("base_url"),
            "backing_health_url": config.provider_health_url(self.provider_name),
            "vector_store_type": self.vector_store_type,
            "timeout": provider_kwargs.get("timeout"),
            "max_retries": provider_kwargs.get("max_retries"),
        }

    def provider_health(self) -> dict[str, Any]:
        """Probe the backing model server health endpoint when configured."""

        health_url = config.provider_health_url(self.provider_name)
        if not health_url:
            return {"status": "unknown", "reason": "no_health_url"}

        timeout = _gateway_health_timeout()
        started_at = time.perf_counter()
        try:
            request = Request(health_url, method="GET")
            with urlopen(request, timeout=timeout) as response:  # nosec B310
                status_code = int(getattr(response, "status", 0) or 0)
        except HTTPError as exc:
            status_code = exc.code
            status = "degraded"
        except (OSError, URLError, TimeoutError) as exc:
            return {
                "status": "degraded",
                "url": health_url,
                "latency_ms": _elapsed_ms(started_at),
                "reason": exc.__class__.__name__,
            }
        except Exception as exc:
            logger.debug("Provider health check failed unexpectedly.")
            return {
                "status": "degraded",
                "url": health_url,
                "latency_ms": _elapsed_ms(started_at),
                "reason": exc.__class__.__name__,
            }
        else:
            status = "ok" if status_code < 400 else "degraded"

        return {
            "status": status,
            "url": health_url,
            "http_status": status_code,
            "latency_ms": _elapsed_ms(started_at),
        }

    def log_request(self, metadata: dict[str, Any], *, failed: bool = False) -> None:
        """Log one gateway request to MLflow with raw prompt fields stripped."""

        tags = {
            "run_type": "gateway",
            "provider": str(metadata.get("backing_provider") or ""),
            "model": str(metadata.get("backing_model") or ""),
            "failed": str(failed).lower(),
        }
        metrics = {
            "latency_ms": metadata.get("latency_ms"),
            "retrieval_count": metadata.get("retrieval_count"),
        }
        record = {
            "query_id": metadata.get("request_id"),
            "question": metadata.get("_question", ""),
            "retrieved_doc_ids": metadata.get("retrieved_doc_ids", []),
            "latency_ms": metadata.get("latency_ms"),
        }
        sanitized = mlflow_tracker.sanitize_prompt_record(
            record,
            top_k=int(config.MLFLOW.artifact_top_k),
            include_answer=False,
        )
        sanitized.update(
            {
                "request_id": metadata.get("request_id"),
                "provider": metadata.get("backing_provider"),
                "backing_model": metadata.get("backing_model"),
                "prompt_hash": metadata.get("prompt_hash"),
                "completion_hash": metadata.get("completion_hash"),
                "error_type": metadata.get("error_type"),
            }
        )
        safe_metadata = {
            key: value
            for key, value in metadata.items()
            if not key.startswith("_") and key not in {"retrieved_doc_ids"}
        }
        with mlflow_tracker.start_run(
            run_name=f"gateway:{metadata.get('prompt_hash')}",
            tags=tags,
        ):
            mlflow_tracker.log_params(safe_metadata)
            mlflow_tracker.log_metrics(metrics)
            mlflow_tracker.log_jsonl([sanitized], "gateway/requests.jsonl")

    def new_request_id(self) -> str:
        """Return an opaque request identifier suitable for logs and clients."""

        return f"rag-{uuid.uuid4().hex}"

    def _get_chain(self) -> Any:
        if self._chain_instance is None:
            self._chain_instance = self._chain_factory()
        return self._chain_instance

    def _metadata(
        self,
        *,
        question: str,
        request_id: str,
        sources: list[dict[str, Any]],
        started_at: float,
    ) -> dict[str, Any]:
        metadata = self._base_metadata(
            question=question,
            request_id=request_id,
            sources=sources,
        )
        metadata["latency_ms"] = _elapsed_ms(started_at)
        return metadata

    def _base_metadata(
        self,
        *,
        question: str,
        request_id: str,
        sources: list[dict[str, Any]],
    ) -> dict[str, Any]:
        provider_metadata = self.provider_metadata()
        retrieved_doc_ids = _retrieved_doc_ids(sources)
        return {
            "request_id": request_id,
            "prompt_hash": mlflow_tracker.hash_text(question),
            "retrieval_count": len(sources),
            "retrieved_doc_ids": retrieved_doc_ids,
            "_question": question,
            **provider_metadata,
        }


def normalize_rag_answer(result: Any) -> str:
    """Normalize LangChain/string RAG outputs to a response string."""

    if isinstance(result, dict) and "answer" in result:
        answer = result.get("answer")
        return "" if answer is None else str(answer)
    return "" if result is None else str(result)


def extract_rag_sources(result: Any) -> list[dict[str, Any]]:
    """Extract stable, deduplicated source metadata from RAG context docs."""

    if not isinstance(result, dict):
        return []

    sources: list[dict[str, Any]] = []
    seen: set[str] = set()
    for doc in result.get("context") or []:
        source = _source_from_doc(doc)
        if not source:
            continue
        dedupe_key = (
            source.get("chunk_id")
            or source.get("id")
            or source.get("source")
            or source.get("snippet")
        )
        if dedupe_key:
            key = str(dedupe_key)
            if key in seen:
                continue
            seen.add(key)
        sources.append(source)
    return sources


def _default_rag_chain_factory() -> Any:
    """Build the default RAG chain lazily so health checks stay lightweight."""

    from src.rag.rag_pipeline import create_rag_chain

    provider_name = os.environ.get("RAG_GATEWAY_LLM_PROVIDER", DEFAULT_GATEWAY_PROVIDER)
    vector_store_type = os.environ.get("RAG_GATEWAY_VECTOR_STORE", DEFAULT_VECTOR_STORE)
    return create_rag_chain(
        llm_provider_name=provider_name,
        vector_store_type=vector_store_type,
    )


def _source_from_doc(doc: Any) -> dict[str, Any]:
    metadata = getattr(doc, "metadata", {}) or {}
    page_content = getattr(doc, "page_content", "") or ""
    source: dict[str, Any] = {}

    field_map = {
        "id": ("id", "document_id", "doc_id"),
        "source": ("source", "path", "file_path"),
        "title": ("title", "source_title", "name"),
        "url": ("url", "canonical_url", "source_url"),
        "chunk_id": ("chunk_id",),
        "score": ("score", "relevance_score"),
        "source_id": ("source_id",),
        "source_title": ("source_title",),
        "organization_or_maintainer": ("organization_or_maintainer",),
        "canonical_url": ("canonical_url",),
        "source_group": ("source_group",),
        "source_type": ("source_type",),
        "trust_tier": ("trust_tier",),
        "authority_scope": ("authority_scope",),
        "topic_tags": ("topic_tags", "tags"),
        "local_conflict_risk": ("local_conflict_risk",),
        "cluster_specific": ("cluster_specific",),
        "cluster_specific_fields_detected": ("cluster_specific_fields_detected",),
        "example_only": ("example_only",),
        "license_note": ("license_note",),
        "retrieval_weight": ("retrieval_weight",),
    }
    for output_key, metadata_keys in field_map.items():
        value = _first_metadata_value(metadata, metadata_keys)
        if value is not None and value != "":
            source[output_key] = value

    snippet = " ".join(str(page_content).split())[:SOURCE_SNIPPET_CHARS]
    if snippet:
        source["snippet"] = snippet
    return source


def _first_metadata_value(metadata: dict[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        value = metadata.get(key)
        if value is not None and value != "":
            return value
    return None


def _retrieved_doc_ids(sources: list[dict[str, Any]]) -> list[str]:
    ids = []
    for source in sources:
        doc_id = source.get("chunk_id") or source.get("id") or source.get("source")
        if doc_id:
            ids.append(str(doc_id))
    return ids


def _elapsed_ms(started_at: float) -> float:
    return round((time.perf_counter() - started_at) * 1000.0, 2)


def _gateway_health_timeout() -> float:
    raw_value = os.environ.get("RAG_GATEWAY_PROVIDER_HEALTH_TIMEOUT", "0.5")
    try:
        return max(0.05, float(raw_value))
    except ValueError:
        return 0.5
