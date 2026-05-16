"""Tests for source-authority retrieval policy."""

from __future__ import annotations

from typing import Any

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from src.rag.retrieval_policy import SourcePriorityRetriever, prioritize_documents


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


def test_slurm_docs_outrank_external_examples_for_slurm_behavior() -> None:
    slurm = FakeDoc({"source_id": "slurm_documentation", "source_group": "reference"})
    external = FakeDoc({"source_id": "yale_ycrc_docs", "source_group": "external_hpc"})

    docs = prioritize_documents([external, slurm], "What does sbatch --array do in Slurm?")

    assert docs == [slurm, external]


def test_official_docs_outrank_external_hpc_for_general_tool_behavior() -> None:
    official = FakeDoc({"source_id": "pip_user_guide", "source_group": "official"})
    external = FakeDoc({"source_id": "princeton_research_computing_kb", "source_group": "external_hpc"})

    docs = prioritize_documents([external, official], "How do pip constraints files work?")

    assert docs == [official, external]


def test_source_priority_retriever_can_be_used_as_langchain_callable() -> None:
    """LangChain hashes runnable callables while resolving config specs."""

    docs = [FakeDoc({"source_id": "slurm_documentation", "source_group": "reference"})]
    docs[0].page_content = "Submit batch jobs with sbatch."
    retriever = SourcePriorityRetriever(RunnableLambda(lambda _: docs))
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | RunnablePassthrough.assign(
            answer=RunnableLambda(lambda _: "Use sbatch.")
        )
    )

    result = chain.invoke("How do I submit a Slurm batch job?")

    assert result["answer"] == "Use sbatch."
    assert result["context"] == docs
