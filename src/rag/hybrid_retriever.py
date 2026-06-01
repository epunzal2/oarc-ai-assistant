"""Opt-in hybrid retrieval with keyword merge, authority policy, and reranking.

The default gateway path remains vector-only. This module is used when
`RAG_RETRIEVAL_MODE=hybrid` or tests explicitly instantiate it.
"""

from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass
from typing import Any, Callable

from src.rag.logger import get_logger
from src.rag.retrieval_policy import prioritize_documents

logger = get_logger(__name__)
_NAMED_LOCAL_GUIDE_RE = re.compile(
    r"\baccording to the\s+(?:oarc\s+)?(?P<name>[a-z0-9][a-z0-9 -]{2,80}?)\s+guide\b",
    re.IGNORECASE,
)
_DISTINCTIVE_STOPWORDS = {
    "amarel",
    "batch",
    "cluster",
    "command",
    "compute",
    "guide",
    "help",
    "hpc",
    "job",
    "jobs",
    "oarc",
    "partition",
    "partitions",
    "policy",
    "queue",
    "rutgers",
    "scheduler",
    "script",
    "slurm",
    "submit",
    "support",
}


@dataclass(frozen=True)
class RetrievalSettings:
    """Runtime knobs for candidate retrieval, optional reranking, and final context."""

    retrieval_mode: str = "hybrid"
    vector_top_k: int = 20
    keyword_top_k: int = 20
    rerank_top_k: int = 8
    final_top_k: int = 4
    reranker_enabled: bool = False
    reranker_required: bool = False
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker:
    """Lazy wrapper around `sentence_transformers.CrossEncoder` for CPU-friendly reranking."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: Any = None

    def rank(self, query: str, docs: list[Any], *, top_k: int) -> list[Any]:
        """Return documents ordered by descending cross-encoder relevance score."""

        if not docs:
            return []
        model = self._load()
        pairs = [(query, str(getattr(doc, "page_content", "") or "")) for doc in docs]
        scores = model.predict(pairs)
        ranked = sorted(
            zip(scores, docs),
            key=lambda item: float(item[0]),
            reverse=True,
        )
        return [doc for _, doc in ranked[:top_k]]

    def _load(self) -> Any:
        if self._model is None:
            from sentence_transformers import CrossEncoder  # type: ignore

            self._model = CrossEncoder(self.model_name)
        return self._model


class HybridRetriever:
    """Merge vector and keyword candidates, dedupe them, and emit diagnostics."""

    applies_source_policy = True

    def __init__(
        self,
        *,
        vector_retriever: Any,
        keyword_retriever: Any,
        settings: RetrievalSettings | None = None,
        reranker: Any | None = None,
        reranker_factory: Callable[[], Any] | None = None,
    ) -> None:
        self.vector_retriever = vector_retriever
        self.keyword_retriever = keyword_retriever
        self.settings = settings or RetrievalSettings()
        self.reranker = reranker
        self.reranker_factory = reranker_factory
        self.last_retrieval_diagnostics: dict[str, Any] = {}

    def invoke(self, query: str) -> list[Any]:
        retrieval_started = time.perf_counter()
        vector_docs = _invoke_retriever(self.vector_retriever, query)
        raw_keyword_docs = _invoke_retriever(self.keyword_retriever, query)
        keyword_docs = filter_keyword_candidates(query, raw_keyword_docs)
        retrieval_latency_ms = _elapsed_ms(retrieval_started)

        merged = merge_documents([*vector_docs, *keyword_docs])
        policy_ranked = prioritize_documents(merged, query)

        rerank_started = time.perf_counter()
        reranked_count = 0
        candidates = policy_ranked
        if self.settings.reranker_enabled:
            candidates = self._rerank(query, policy_ranked[: self.settings.rerank_top_k])
            reranked_count = len(candidates)
        rerank_latency_ms = _elapsed_ms(rerank_started)

        final_docs = candidates[: self.settings.final_top_k]
        self.last_retrieval_diagnostics = {
            "retrieval_mode": self.settings.retrieval_mode,
            "vector_candidate_count": len(vector_docs),
            "keyword_candidate_count": len(raw_keyword_docs),
            "keyword_filtered_count": len(raw_keyword_docs) - len(keyword_docs),
            "merged_count": len(merged),
            "reranked_count": reranked_count,
            "final_count": len(final_docs),
            "retrieval_latency_ms": retrieval_latency_ms,
            "rerank_latency_ms": rerank_latency_ms,
            "final_source_ids": [source_id_for_doc(doc) for doc in final_docs],
        }
        return final_docs

    def get_relevant_documents(self, query: str) -> list[Any]:
        return self.invoke(query)

    def __call__(self, query: str) -> list[Any]:
        return self.invoke(query)

    def _rerank(self, query: str, docs: list[Any]) -> list[Any]:
        try:
            reranker = self.reranker
            if reranker is None:
                factory = self.reranker_factory or (
                    lambda: CrossEncoderReranker(self.settings.reranker_model)
                )
                reranker = factory()
                self.reranker = reranker
            return list(reranker.rank(query, docs, top_k=self.settings.rerank_top_k))
        except Exception:
            if self.settings.reranker_required:
                raise
            logger.warning("RAG reranker unavailable; using authority-ranked merged results.")
            return docs


def merge_documents(docs: list[Any]) -> list[Any]:
    """Dedupe retrieved documents while preserving first-seen rank order."""

    merged: list[Any] = []
    seen: set[str] = set()
    for doc in docs:
        identity = doc_identity(doc)
        if identity in seen:
            continue
        seen.add(identity)
        merged.append(doc)
    return merged


def filter_keyword_candidates(query: str, docs: list[Any]) -> list[Any]:
    """Drop keyword candidates that miss distinctive named local-guide terms."""

    distinctive_terms = _distinctive_named_terms(query)
    if len(distinctive_terms) < 2:
        return docs
    filtered = [
        doc
        for doc in docs
        if _doc_contains_any_term(doc, distinctive_terms)
    ]
    return filtered


def doc_identity(doc: Any) -> str:
    """Return a stable dedupe identity for a retrieved document."""

    metadata = getattr(doc, "metadata", {}) or {}
    for prefix, key in (
        ("chunk", "chunk_id"),
        ("source", "source"),
        ("hash", "content_hash"),
    ):
        value = metadata.get(key)
        if value:
            return f"{prefix}:{value}"
    content = str(getattr(doc, "page_content", "") or "")
    digest = hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()[:16]
    return f"content:{digest}"


def source_id_for_doc(doc: Any) -> str:
    """Return a compact source identifier safe for response diagnostics."""

    metadata = getattr(doc, "metadata", {}) or {}
    for key in ("chunk_id", "id", "document_id", "source", "content_hash"):
        value = metadata.get(key)
        if value:
            return str(value)
    return doc_identity(doc)


def retrieval_diagnostics(retriever: Any) -> dict[str, Any]:
    """Return last retrieval diagnostics from wrapped retrievers when present."""

    current = retriever
    visited: set[int] = set()
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        diagnostics = getattr(current, "last_retrieval_diagnostics", None)
        if isinstance(diagnostics, dict) and diagnostics:
            return dict(diagnostics)
        current = getattr(current, "retriever", None)
    return {}


def _invoke_retriever(retriever: Any, query: str) -> list[Any]:
    if hasattr(retriever, "invoke"):
        return list(retriever.invoke(query))
    if hasattr(retriever, "get_relevant_documents"):
        return list(retriever.get_relevant_documents(query))
    return list(retriever(query))


def _distinctive_named_terms(query: str) -> list[str]:
    match = _NAMED_LOCAL_GUIDE_RE.search(str(query or ""))
    if not match:
        return []
    return [
        term
        for term in re.findall(r"[a-z0-9]+", match.group("name").lower())
        if term not in _DISTINCTIVE_STOPWORDS
    ]


def _doc_contains_any_term(doc: Any, terms: list[str]) -> bool:
    metadata = getattr(doc, "metadata", {}) or {}
    text = " ".join(
        [
            str(getattr(doc, "page_content", "") or ""),
            " ".join(str(value) for value in metadata.values()),
        ]
    ).lower()
    return any(term in text for term in terms)


def _elapsed_ms(started_at: float) -> float:
    return round((time.perf_counter() - started_at) * 1000.0, 2)


__all__ = [
    "CrossEncoderReranker",
    "HybridRetriever",
    "RetrievalSettings",
    "doc_identity",
    "filter_keyword_candidates",
    "merge_documents",
    "retrieval_diagnostics",
    "source_id_for_doc",
]
