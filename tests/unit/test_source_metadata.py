"""Tests for source metadata enrichment and cluster-specific detection."""

from __future__ import annotations

from pathlib import Path

from src.rag.source_manifest import CONFIG_PATH, SourceManifest
from src.rag.source_metadata import (
    detect_cluster_specific_fields,
    infer_source_metadata_from_path,
    metadata_for_source,
)


def test_cluster_specific_detector_finds_expected_field_categories() -> None:
    text = """
    Use /scratch/project for temporary files. Submit with #SBATCH --partition=gpu
    and module load cuda/12.1. Connect to login.example.edu, then email hpc@example.edu
    for quota, purge, MFA, VPN, and sensitive data policy questions.
    """

    fields = set(detect_cluster_specific_fields(text))

    assert {
        "paths",
        "scheduling",
        "modules",
        "hostnames",
        "support",
        "quotas",
        "access_policy",
        "data_policy",
    } <= fields


def test_external_hpc_metadata_stays_example_only_when_cluster_specific() -> None:
    manifest = SourceManifest.from_file(CONFIG_PATH)
    nersc = manifest.source_by_id()["nersc_docs"]

    metadata = metadata_for_source(
        nersc,
        canonical_url="https://docs.nersc.gov/example/",
        content="Run on /global/cfs and choose a queue.",
    )

    assert metadata["source_id"] == "nersc_docs"
    assert metadata["source_group"] == "external_hpc"
    assert metadata["example_only"] is True
    assert metadata["cluster_specific"] is True
    assert "paths" in metadata["cluster_specific_fields_detected"]


def test_path_inference_marks_local_guide_and_slurm_authorities(tmp_path: Path) -> None:
    local_path = tmp_path / "docs" / "google_sites_guide" / "cluster_user_guide.md"
    slurm_path = tmp_path / "docs" / "slurm-23.02.7" / "markdown" / "man" / "sbatch.md"

    local = infer_source_metadata_from_path(local_path, content="Use /scratch for jobs.")
    slurm = infer_source_metadata_from_path(slurm_path, content="sbatch submits jobs.")

    assert local["source_id"] == "local_university_hpc_guide"
    assert local["source_group"] == "local"
    assert local["example_only"] is False
    assert slurm["source_id"] == "slurm_documentation"
    assert slurm["source_group"] == "reference"
    assert "slurm_syntax" in slurm["authority_scope"]
