"""Tests for opt-in hybrid retrieval and reranking."""

from __future__ import annotations

from typing import Any

import pytest

from src.rag.hybrid_retriever import HybridRetriever, RetrievalSettings, doc_identity
from src.rag.retrieval_policy import SourcePriorityRetriever


class FakeDoc:
    """Minimal document carrying content and metadata."""

    def __init__(self, text: str, metadata: dict[str, Any]) -> None:
        self.page_content = text
        self.metadata = metadata


class ListRetriever:
    """Retriever fake returning a fixed list of documents."""

    def __init__(self, docs: list[FakeDoc]) -> None:
        self.docs = docs

    def invoke(self, query: str) -> list[FakeDoc]:
        return list(self.docs)


class OrderingReranker:
    """Reranker fake that orders documents by a metadata field."""

    def rank(self, query: str, docs: list[FakeDoc], *, top_k: int) -> list[FakeDoc]:
        return sorted(docs, key=lambda doc: doc.metadata.get("rank", 99))[:top_k]


def test_doc_identity_prefers_chunk_source_hash_then_content() -> None:
    assert doc_identity(FakeDoc("text", {"chunk_id": "c1", "source": "s"})) == "chunk:c1"
    assert doc_identity(FakeDoc("text", {"source": "s"})) == "source:s"
    assert doc_identity(FakeDoc("text", {"content_hash": "h"})) == "hash:h"
    assert doc_identity(FakeDoc("text", {})).startswith("content:")


def test_hybrid_retriever_merges_dedupes_applies_policy_and_limits_final_docs() -> None:
    local = FakeDoc(
        "Local Amarel scratch guidance",
        {"chunk_id": "local", "source_group": "local", "rank": 2},
    )
    duplicate = FakeDoc(
        "Duplicate from keyword",
        {"chunk_id": "local", "source_group": "local", "rank": 1},
    )
    external = FakeDoc(
        "External cluster-specific scratch guidance",
        {"chunk_id": "external", "source_group": "external_hpc", "cluster_specific": True},
    )
    official = FakeDoc(
        "Official Slurm command reference",
        {"chunk_id": "official", "source_id": "slurm_documentation", "source_group": "reference"},
    )
    retriever = HybridRetriever(
        vector_retriever=ListRetriever([external, local]),
        keyword_retriever=ListRetriever([duplicate, official]),
        settings=RetrievalSettings(final_top_k=2, rerank_top_k=3),
    )

    docs = retriever.invoke("What is the local scratch path on Amarel?")

    assert [doc.metadata["chunk_id"] for doc in docs] == ["local", "official"]
    assert retriever.last_retrieval_diagnostics["vector_candidate_count"] == 2
    assert retriever.last_retrieval_diagnostics["keyword_candidate_count"] == 2
    assert retriever.last_retrieval_diagnostics["merged_count"] == 3
    assert retriever.last_retrieval_diagnostics["final_count"] == 2
    assert retriever.applies_source_policy is True


def test_hybrid_retriever_uses_reranker_when_enabled() -> None:
    slow = FakeDoc("slow", {"chunk_id": "slow", "rank": 2})
    fast = FakeDoc("fast", {"chunk_id": "fast", "rank": 1})
    retriever = HybridRetriever(
        vector_retriever=ListRetriever([slow]),
        keyword_retriever=ListRetriever([fast]),
        settings=RetrievalSettings(final_top_k=1, rerank_top_k=2, reranker_enabled=True),
        reranker=OrderingReranker(),
    )

    docs = retriever.invoke("query")

    assert [doc.metadata["chunk_id"] for doc in docs] == ["fast"]
    assert retriever.last_retrieval_diagnostics["reranked_count"] == 2


def test_hybrid_retriever_filters_keyword_noise_for_distinctive_named_queries() -> None:
    vector = FakeDoc("Generic Slurm submit guidance", {"chunk_id": "vector", "rank": 1})
    keyword_noise = FakeDoc("Applications and partitions overview", {"chunk_id": "keyword"})
    retriever = HybridRetriever(
        vector_retriever=ListRetriever([vector]),
        keyword_retriever=ListRetriever([keyword_noise]),
        settings=RetrievalSettings(final_top_k=4),
    )

    docs = retriever.invoke(
        "According to the OARC quantum dragon partition guide, "
        "how do I submit to that partition?"
    )

    assert [doc.metadata["chunk_id"] for doc in docs] == ["vector"]
    assert retriever.last_retrieval_diagnostics["keyword_candidate_count"] == 1
    assert retriever.last_retrieval_diagnostics["keyword_filtered_count"] == 1


def test_hybrid_retriever_raises_when_required_reranker_is_missing() -> None:
    retriever = HybridRetriever(
        vector_retriever=ListRetriever([]),
        keyword_retriever=ListRetriever([]),
        settings=RetrievalSettings(reranker_enabled=True, reranker_required=True),
        reranker_factory=lambda: (_ for _ in ()).throw(RuntimeError("missing model")),
    )

    with pytest.raises(RuntimeError, match="missing model"):
        retriever.invoke("query")


def test_source_priority_retriever_records_diagnostics_for_vector_only_path() -> None:
    docs = [FakeDoc("Submit with sbatch", {"chunk_id": "slurm", "source_id": "slurm_documentation"})]
    retriever = SourcePriorityRetriever(ListRetriever(docs))

    result = retriever.invoke("How do I submit a Slurm job?")

    assert result == docs
    assert retriever.last_retrieval_diagnostics["final_count"] == 1
    assert retriever.last_retrieval_diagnostics["final_source_ids"] == ["slurm"]
