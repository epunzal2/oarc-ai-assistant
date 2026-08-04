"""Tests for source-authority retrieval policy."""

from __future__ import annotations

from typing import Any

from src.rag.retrieval_policy import (
    LocalGuideFallbackRetriever,
    SourcePriorityRetriever,
    explicitly_allows_external_examples,
    forces_local_guide_fallback,
    is_local_operational_query,
    needs_local_guide_fallback,
    prioritize_documents,
)


class FakeDoc:
    """Minimal document carrying metadata for retriever policy tests."""

    def __init__(self, metadata: dict[str, Any]) -> None:
        self.page_content = "content"
        self.metadata = metadata


def test_local_operational_queries_suppress_external_hpc_examples() -> None:
    local = FakeDoc({"source_id": "local_university_hpc_guide", "source_group": "local"})
    external = FakeDoc(
        {
            "source_id": "nersc_docs",
            "source_group": "external_hpc",
            "example_only": True,
            "cluster_specific": True,
        }
    )

    docs = prioritize_documents([external, local], "What is the local scratch quota?")

    assert docs == [local]


def test_explicit_example_queries_can_keep_external_hpc_docs() -> None:
    external = FakeDoc(
        {
            "source_id": "nersc_docs",
            "source_group": "external_hpc",
            "example_only": True,
            "cluster_specific": True,
        }
    )

    docs = prioritize_documents([external], "Show an external example for troubleshooting jobs")

    assert docs == [external]


def test_external_collaborator_access_is_not_an_external_example_query() -> None:
    query = "Can an external collaborator use Amarel resources owned by a Rutgers group?"

    assert not explicitly_allows_external_examples(query)
    assert needs_local_guide_fallback(query)
    assert forces_local_guide_fallback(query)


def test_slurm_docs_outrank_external_examples_for_slurm_behavior() -> None:
    slurm = FakeDoc({"source_id": "slurm_documentation", "source_group": "reference"})
    external = FakeDoc({"source_id": "yale_ycrc_docs", "source_group": "external_hpc"})

    docs = prioritize_documents([external, slurm], "What does sbatch --array do in Slurm?")

    assert docs == [slurm, external]


def test_compute_node_interactive_questions_are_local_operational_queries() -> None:
    query = "How do I start a quick interactive command on a Slurm compute node?"

    assert is_local_operational_query(query)
    assert needs_local_guide_fallback(query)


def test_local_guide_fallback_augments_vector_docs_for_forced_local_policy_questions() -> None:
    slurm = FakeDoc({"chunk_id": "slurm", "source_id": "slurm_documentation"})
    primary_local = FakeDoc(
        {
            "chunk_id": "welcome",
            "source_group": "local",
            "source_id": "local_university_hpc_guide",
        }
    )
    local = FakeDoc(
        {
            "chunk_id": "cluster_user_guide",
            "source": "docs/google_sites_guide/cluster_user_guide.md",
            "source_group": "local",
            "source_id": "local_university_hpc_guide",
        }
    )
    retriever = LocalGuideFallbackRetriever(
        retriever=lambda _: [slurm, primary_local],
        fallback_retriever=lambda _: [local],
        final_top_k=3,
    )

    docs = retriever.invoke("Can an external collaborator use Amarel owned resources?")

    assert docs == [local, primary_local, slurm]
    assert retriever.last_retrieval_diagnostics["local_fallback_needed"] is True
    assert retriever.last_retrieval_diagnostics["local_fallback_count"] == 1
    assert retriever.last_retrieval_diagnostics["final_source_ids"] == [
        "cluster_user_guide",
        "welcome",
        "slurm",
    ]


def test_login_node_fallback_is_skipped_when_vector_already_has_local_docs() -> None:
    primary_local = FakeDoc(
        {
            "chunk_id": "cluster_login",
            "source_group": "local",
            "source_id": "local_university_hpc_guide",
        }
    )
    fallback_local = FakeDoc(
        {
            "chunk_id": "cluster_other",
            "source_group": "local",
            "source_id": "local_university_hpc_guide",
        }
    )
    retriever = LocalGuideFallbackRetriever(
        retriever=lambda _: [primary_local],
        fallback_retriever=lambda _: [fallback_local],
        final_top_k=2,
    )

    docs = retriever.invoke("Can I run heavy computations on an Amarel login node?")

    assert docs == [primary_local]
    assert retriever.last_retrieval_diagnostics["local_fallback_needed"] is False
    assert retriever.last_retrieval_diagnostics["local_fallback_count"] == 0


def test_interactive_fallback_runs_when_vector_has_only_slurm_docs() -> None:
    slurm = FakeDoc({"chunk_id": "slurm", "source_id": "slurm_documentation"})
    local = FakeDoc(
        {
            "chunk_id": "cluster_interactive",
            "source_group": "local",
            "source_id": "local_university_hpc_guide",
        }
    )
    retriever = LocalGuideFallbackRetriever(
        retriever=lambda _: [slurm],
        fallback_retriever=lambda _: [local],
        final_top_k=2,
    )

    docs = retriever.invoke("How do I start a quick interactive command on a Slurm compute node?")

    assert docs == [local, slurm]
    assert retriever.last_retrieval_diagnostics["local_fallback_needed"] is True


def test_official_docs_outrank_external_hpc_for_general_tool_behavior() -> None:
    official = FakeDoc({"source_id": "pip_user_guide", "source_group": "official"})
    external = FakeDoc({"source_id": "princeton_research_computing_kb", "source_group": "external_hpc"})

    docs = prioritize_documents([external, official], "How do pip constraints files work?")

    assert docs == [official, external]


def test_source_priority_retriever_can_wrap_plain_callables() -> None:
    """The policy wrapper supports callable retrievers used by lightweight tests."""

    docs = [FakeDoc({"source_id": "slurm_documentation", "source_group": "reference"})]
    docs[0].page_content = "Submit batch jobs with sbatch."
    retriever = SourcePriorityRetriever(lambda _: docs)

    result = retriever("How do I submit a Slurm batch job?")

    assert result == docs
