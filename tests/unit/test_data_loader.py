"""Tests for RAG data loader metadata enrichment."""

from __future__ import annotations

import os
from pathlib import Path

from src.rag.data_loader import chunk_documents, load_markdown_documents


def test_load_markdown_documents_supports_path_lists_and_front_matter(tmp_path: Path) -> None:
    local_root = tmp_path / "docs" / "google_sites_guide"
    imported_root = tmp_path / "docs" / "corpus" / "staging" / "hpc"
    local_root.mkdir(parents=True)
    imported_root.mkdir(parents=True)
    (local_root / "guide.md").write_text("# Guide\n\nUse /scratch for jobs.\n", encoding="utf-8")
    (imported_root / "bash.md").write_text(
        """---
source_id: "gnu_bash_reference_manual"
source_title: "GNU Bash Reference Manual"
source_group: "official"
trust_tier: "Tier 1"
retrieval_weight: 1.0
example_only: false
---

# Bash

Shell expansion reference.
""",
        encoding="utf-8",
    )

    docs = load_markdown_documents(f"{local_root}{os.pathsep}{imported_root}")
    by_source_id = {doc.metadata.get("source_id"): doc for doc in docs}

    assert by_source_id["local_university_hpc_guide"].metadata["source_group"] == "local"
    assert by_source_id["local_university_hpc_guide"].metadata["cluster_specific"] is True
    assert by_source_id["gnu_bash_reference_manual"].metadata["source_group"] == "official"
    assert "---" not in by_source_id["gnu_bash_reference_manual"].page_content


def test_chunk_documents_adds_stable_chunk_metadata(tmp_path: Path) -> None:
    corpus = tmp_path / "docs" / "google_sites_guide"
    corpus.mkdir(parents=True)
    (corpus / "guide.md").write_text("# Guide\n\nUse sbatch for jobs.\n", encoding="utf-8")
    docs = load_markdown_documents(corpus)

    chunks = chunk_documents(docs)

    assert chunks
    assert chunks[0].metadata["chunk_id"].startswith("local_university_hpc_guide:")
    assert chunks[0].metadata["content_hash"]
