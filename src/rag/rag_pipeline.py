"""LangChain RAG chain construction and runtime instrumentation."""

from typing import Callable, Iterable, Optional, Dict, Any
import os
import hashlib
import itertools
import json
import random
import time
from pathlib import Path

try:  # pragma: no cover - optional dependency
    import mlflow
except Exception:  # pragma: no cover - optional dependency
    mlflow = None

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

try:
    import tiktoken  # type: ignore
    _ENCODING = tiktoken.get_encoding("cl100k_base")
except Exception:  # pragma: no cover - optional dependency
    _ENCODING = None

from src.rag import mlflow_tracker
from src.rag.vector_store import (
    get_embedding_model,
    get_keyword_retriever,
    get_vector_store,
    load_faiss_index,
)
from src.rag.llm_provider import get_llm_provider
from src.rag.logger import get_logger
from src.rag import config
from src.rag.telemetry import get_sampler
from src.rag.retrieval_policy import maybe_wrap_retriever

logger = get_logger(__name__)


class InstrumentedRAGChain:
    """Wraps a LangChain runnable with MLflow + telemetry instrumentation."""

    def __init__(
        self,
        chain,
        *,
        provider_name: str,
        model_name: str,
        vector_store_type: str,
        prompt_template: str,
        retriever_descriptor: Dict[str, Any],
        index_version: str,
        corpus_hash: str,
        provider_config_path: Optional[Path],
        stream_answer: Optional[Callable[[str], Dict[str, Any]]] = None,
    ) -> None:
        self._chain = chain
        self._stream_answer = stream_answer
        self.provider_name = provider_name
        self.model_name = model_name
        self.vector_store_type = vector_store_type
        self.prompt_template = prompt_template
        self.prompt_version = mlflow_tracker.hash_text(prompt_template)
        self.retriever_descriptor = retriever_descriptor
        self.retriever_version = self._hash_config(retriever_descriptor)
        self.index_version = index_version
        self.corpus_hash = corpus_hash
        self.provider_config_path = provider_config_path
        self.sample_probability = max(0.0, min(1.0, config.MLFLOW.runtime_sampling_probability))
        self.artifact_top_k = mlflow_tracker.config.MLFLOW.artifact_top_k
        self._sampler = get_sampler()
        self._sampler.start()
        self._counter = itertools.count()

    def invoke(self, prompt: str, **kwargs):
        start = time.perf_counter()
        result = self._chain.invoke(prompt, **kwargs)
        latency_ms = (time.perf_counter() - start) * 1000.0
        if not self._should_sample():
            return result

        context_docs = []
        answer = result
        if isinstance(result, dict):
            context_docs = result.get("context") or []
            answer = result.get("answer")

        retrieved_ids = []
        for doc in context_docs:
            metadata = getattr(doc, "metadata", {}) or {}
            doc_id = (
                metadata.get("chunk_id")
                or metadata.get("id")
                or metadata.get("document_id")
                or metadata.get("source")
            )
            if doc_id:
                retrieved_ids.append(str(doc_id))

        record = {
            "query_id": f"req{next(self._counter)}",
            "question": prompt,
            "answer": answer,
            "retrieved_doc_ids": retrieved_ids,
        }
        sanitized = mlflow_tracker.sanitize_prompt_record(
            record,
            top_k=min(self.artifact_top_k, len(retrieved_ids)),
            include_answer=True,
        )
        sanitized["latency_ms"] = round(latency_ms, 2)
        run_name = f"runtime:{sanitized['prompt_hash']}"
        tags = {
            "run_type": "runtime",
            "provider": self.provider_name,
            "model": self.model_name,
            "index_version": self.index_version,
            "prompt_version": self.prompt_version,
            "retriever_version": self.retriever_version,
            "corpus_hash": self.corpus_hash,
        }
        telemetry_samples = self._sampler.flush()
        metrics = {
            "latency_ms": latency_ms,
            "retrieval_count": len(retrieved_ids),
            "runtime_sampling_probability": self.sample_probability,
        }
        if telemetry_samples:
            last_sample = telemetry_samples[-1]
            for key, value in last_sample.items():
                if isinstance(value, (int, float)):
                    metrics[key] = value
        with mlflow_tracker.start_run(run_name=run_name, tags=tags):
            mlflow_tracker.log_params(
                {
                    "vector_store_type": self.vector_store_type,
                    "telemetry_backend": self._sampler.backend,
                    "artifact_top_k": self.artifact_top_k,
                }
            )
            mlflow_tracker.log_metrics(metrics)
            mlflow_tracker.log_jsonl([sanitized], "runtime/responses.jsonl")
            mlflow_tracker.log_dict(self.retriever_descriptor, "runtime/retriever_config.json")
            mlflow_tracker.log_text(self.prompt_template, "runtime/prompt_template.txt")
            if telemetry_samples:
                mlflow_tracker.log_jsonl(telemetry_samples, "runtime/telemetry_samples.jsonl")
            if self.provider_config_path:
                mlflow_tracker.log_artifact_from_path(
                    self.provider_config_path,
                    artifact_path="runtime/provider",
                )
        return result

    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)

    def stream_answer(self, prompt: str) -> Dict[str, Any]:
        """Return retrieved context and an answer chunk iterator for streaming gateways."""
        if self._stream_answer is None:
            raise NotImplementedError("This RAG chain does not expose streaming completions.")
        return self._stream_answer(prompt)

    def __getattr__(self, item):
        return getattr(self._chain, item)

    def _should_sample(self) -> bool:
        if self.sample_probability <= 0.0:
            return False
        if self.sample_probability >= 1.0:
            return True
        return random.random() <= self.sample_probability

    @staticmethod
    def _hash_config(payload: Any) -> str:
        try:
            serialized = json.dumps(payload, sort_keys=True, default=str)
        except (TypeError, ValueError):
            serialized = str(payload)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]

def create_rag_chain(
    llm_provider_name: Optional[str] = None,
    vector_store_type: str = "qdrant",
    retriever=None,
    llm=None,
    llm_provider_kwargs: Optional[Dict[str, Any]] = None,
    max_context_chars: Optional[int] = None,
):
    """Create an instrumented retriever-plus-LLM RAG chain.

    Callers may inject a retriever or LLM for tests/evaluation. When they do
    not, this function resolves the configured vector store and provider from
    environment-backed settings in `src.rag.config`.
    """

    provider_name = (llm_provider_name or config.DEFAULT_LLM_PROVIDER).lower()
    logger.info(
        "Creating RAG chain with LLM provider: %s and vector store: %s...",
        provider_name,
        vector_store_type,
    )
    model_name = provider_name
    provider_config_path: Optional[Path] = None
    llm_provider = None

    # Get the embedding model and vector store
    if retriever is None:
        logger.info("No retriever provided, creating a new one...")
        if vector_store_type == "keyword":
            retriever = get_keyword_retriever()
        else:
            embeddings = get_embedding_model()
        if vector_store_type == "faiss":
            retriever = load_faiss_index(config.FAISS_INDEX_PATH, embeddings)
        elif vector_store_type != "keyword":
            vector_store = get_vector_store(embeddings, vector_store_type=vector_store_type)
            retriever = vector_store.as_retriever()
    else:
        logger.info("Using the provided retriever.")

    retriever = maybe_wrap_retriever(retriever)

    # Get the LLM provider unless an explicit LLM instance was supplied
    if llm is None:
        kwargs: Dict[str, Any] = dict(config.provider_kwargs(provider_name))
        if llm_provider_kwargs:
            kwargs.update(llm_provider_kwargs)
        llm_provider = get_llm_provider(provider_name, **kwargs)
        model_name = (
            kwargs.get("model")
            or kwargs.get("model_name")
            or kwargs.get("model_path")
            or model_name
        )
        try:
            artifact_path = config.persist_provider_settings(
                provider_name, Path("logs/provider_configs")
            )
            if artifact_path:
                provider_config_path = artifact_path
                logger.info("Provider settings persisted to %s", artifact_path)
        except Exception:
            logger.debug("Failed to persist provider settings for %s", provider_name)
        llm = llm_provider.get_llm()

    # Define the prompt template
    template = """
    Answer the following question based on the provided context.
    If the context does not contain the answer, try your best to answer in a general manner and tell the user to refer to 
    the user guide and contact helpdesk support.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # Create the RAG chain
    # Determine caps from environment; tokens take precedence over characters
    # RAG_MAX_CONTEXT_TOKENS: hard limit on context tokens (preferred)
    # RAG_MAX_CONTEXT_CHARS: fallback character cap
    env_tokens = os.environ.get("RAG_MAX_CONTEXT_TOKENS")
    try:
        max_context_tokens = int(env_tokens) if env_tokens else None
    except Exception:
        max_context_tokens = None

    if max_context_chars is None:
        env_cap = os.environ.get("RAG_MAX_CONTEXT_CHARS")
        try:
            max_context_chars = int(env_cap) if env_cap else 12000
        except Exception:
            max_context_chars = 12000

    def _join_trim_by_tokens(docs, token_limit: int) -> str:
        if token_limit <= 0:
            return ""
        if _ENCODING is None:
            # Fallback: conservative char approximation (3 chars/token)
            approx_chars = max(512, token_limit * 3)
            text = "\n\n".join(doc.page_content for doc in docs)
            return text[:approx_chars]
        toks_accum = []
        used = 0
        for doc in docs:
            toks = _ENCODING.encode(doc.page_content)
            if used + len(toks) <= token_limit:
                toks_accum.extend(toks)
                used += len(toks)
            else:
                remaining = max(0, token_limit - used)
                if remaining > 0:
                    toks_accum.extend(toks[:remaining])
                break
        return _ENCODING.decode(toks_accum)

    def format_docs(docs):
        if max_context_tokens:
            return _join_trim_by_tokens(docs, max_context_tokens)
        text = "\n\n".join(doc.page_content for doc in docs)
        if max_context_chars and len(text) > max_context_chars:
            return text[: max_context_chars]
        return text

    def retrieve_docs(question: str):
        if hasattr(retriever, "invoke"):
            return retriever.invoke(question)
        if hasattr(retriever, "get_relevant_documents"):
            return retriever.get_relevant_documents(question)
        return retriever(question)

    def build_prompt_text(question: str, docs) -> str:
        return prompt.format(context=format_docs(docs), question=question)

    def stream_answer(question: str) -> Dict[str, Any]:
        if llm_provider is None:
            raise NotImplementedError("Streaming requires a provider-backed RAG chain.")

        docs = retrieve_docs(question)
        prompt_text = build_prompt_text(question, docs)
        if llm_provider.supports_streaming():
            response = llm_provider.generate(prompt_text, stream=True)
            chunks: Iterable[str] = response.stream or []
        else:
            response = llm_provider.generate(prompt_text, stream=False)
            chunks = [response.text or ""]
        return {"context": docs, "chunks": chunks}

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | RunnablePassthrough.assign(
            answer=(
                RunnablePassthrough.assign(
                    context=(lambda x: format_docs(x["context"]))
                )
                | prompt
                | llm
                | StrOutputParser()
            )
        )
    )

    logger.info("RAG chain created successfully.")
    retriever_descriptor: Dict[str, Any] = {
        "vector_store_type": vector_store_type,
        "embedding_model": config.EMBEDDING_MODEL,
        "custom_retriever": retriever is not None,
        "max_context_tokens": max_context_tokens,
        "max_context_chars": max_context_chars,
    }
    if retriever is not None:
        retriever_descriptor["retriever_cls"] = retriever.__class__.__name__
    if vector_store_type == "qdrant":
        retriever_descriptor.update(
            {
                "qdrant_host": config.QDRANT_HOST,
                "qdrant_port": config.QDRANT_PORT,
                "qdrant_collection": config.QDRANT_COLLECTION_NAME,
            }
        )
        index_descriptor = {
            "type": "qdrant",
            "collection": config.QDRANT_COLLECTION_NAME,
            "host": config.QDRANT_HOST,
            "port": config.QDRANT_PORT,
        }
    else:
        retriever_descriptor["faiss_index_path"] = config.FAISS_INDEX_PATH
        index_descriptor = {
            "type": vector_store_type,
            "faiss_index_path": config.FAISS_INDEX_PATH,
        }
    corpus_descriptor = {
        "data_path": config.DATA_PATH,
        "service_now_path": config.SERVICE_NOW_DATA_PATH,
    }
    index_version = InstrumentedRAGChain._hash_config(index_descriptor)
    corpus_hash = InstrumentedRAGChain._hash_config(corpus_descriptor)
    return InstrumentedRAGChain(
        rag_chain,
        provider_name=provider_name,
        model_name=str(model_name),
        vector_store_type=vector_store_type,
        prompt_template=template,
        retriever_descriptor=retriever_descriptor,
        index_version=index_version,
        corpus_hash=corpus_hash,
        provider_config_path=provider_config_path,
        stream_answer=stream_answer if llm_provider is not None else None,
    )

def log_rag_chain_as_model():
    """Log the default RAG chain as an MLflow model artifact."""

    if mlflow is None:
        raise RuntimeError("MLflow is required to log the RAG chain as a model.")
    mlflow.langchain.autolog()
    with mlflow.start_run():
        rag_chain = create_rag_chain()
        mlflow.pyfunc.log_model(
            artifact_path="rag_chain",
            python_model=rag_chain,
        )
        print("RAG chain logged as an MLflow model.")
        # Test the chain to trigger tracing
        question = "What is the Amarel cluster?"
        rag_chain.invoke(question)
        print("RAG chain invoked to generate traces.")

if __name__ == '__main__':
    log_rag_chain_as_model()
