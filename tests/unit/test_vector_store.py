"""Tests for vector-store helper retrievers."""

from __future__ import annotations

from src.rag.vector_store import get_docstore_keyword_retriever


class FakeDoc:
    """Minimal LangChain-like document for keyword helper tests."""

    def __init__(self, text: str, metadata: dict) -> None:
        self.page_content = text
        self.metadata = metadata


class FakeDocstore:
    """Minimal FAISS docstore shape exposing the private document map."""

    def __init__(self, docs: dict[str, FakeDoc]) -> None:
        self._dict = docs


class FakeVectorStore:
    """Minimal vector-store shape carrying a docstore."""

    def __init__(self, docstore: FakeDocstore) -> None:
        self.docstore = docstore


class FakeRetriever:
    """Minimal LangChain vector retriever shape carrying a vector store."""

    def __init__(self, vectorstore: FakeVectorStore) -> None:
        self.vectorstore = vectorstore


def test_docstore_keyword_retriever_uses_existing_vector_store_documents() -> None:
    retriever = FakeRetriever(
        FakeVectorStore(
            FakeDocstore(
                {
                    "local": FakeDoc(
                        "Interactive jobs use srun on compute nodes.",
                        {"source_id": "local_university_hpc_guide"},
                    ),
                    "slurm": FakeDoc(
                        "The slurmd daemon manages compute nodes.",
                        {"source_id": "slurm_documentation"},
                    ),
                }
            )
        )
    )

    keyword_retriever = get_docstore_keyword_retriever(retriever, k=1)

    assert keyword_retriever is not None
    docs = keyword_retriever.invoke("interactive srun compute nodes")
    assert docs[0].metadata["source_id"] == "local_university_hpc_guide"
