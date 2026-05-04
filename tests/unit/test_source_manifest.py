"""Tests for Research Pro source manifest handling."""

from __future__ import annotations

from pathlib import Path

from src.rag.source_importer import ImportOptions, import_sources
from src.rag.source_manifest import (
    CONFIG_PATH,
    SourceManifest,
    SourceRecord,
    normalize_ingestion_method,
    source_skip_reasons,
)


FIRST_PASS = {
    "gnu_bash_reference_manual",
    "gnu_coreutils_manual",
    "openssh_manual_pages",
    "rsync_documentation",
    "gnu_tar_manual",
    "gnu_gzip_manual",
    "lmod_docs",
    "conda_manage_environments",
    "python_venv_docs",
    "pypa_pip_venv_guide",
    "pip_user_guide",
    "apptainer_user_guide",
    "nersc_docs",
    "princeton_research_computing_kb",
    "yale_ycrc_docs",
}


def test_research_pro_manifest_loads_first_pass_group() -> None:
    manifest = SourceManifest.from_file(CONFIG_PATH)

    selected = manifest.resolve_group("hpc_additional_docs_first_pass")

    assert len(manifest.sources) == 53
    assert {source.source_id for source in selected} == FIRST_PASS
    assert all(source.enabled_by_default is False for source in selected)


def test_ingestion_method_mapping_matches_research_pro_policy() -> None:
    assert normalize_ingestion_method("clone repo") == "git_repo"
    assert normalize_ingestion_method("download rendered static docs or Texinfo") == "static_manual"
    assert normalize_ingestion_method("scrape approved path prefix") == "controlled_website"
    assert normalize_ingestion_method("controlled scrape") == "controlled_website"
    assert normalize_ingestion_method("manual export") == "manual_review"
    assert normalize_ingestion_method("link-only") == "citation_only"
    assert normalize_ingestion_method("review_manually_or_link_only") == "skipped"


def test_skip_reasons_are_conservative_for_license_and_repo_sources() -> None:
    manifest = SourceManifest.from_file(CONFIG_PATH)
    sources = manifest.source_by_id()

    bash = sources["gnu_bash_reference_manual"]
    missing_repo = SourceRecord.from_dict(
        {
            "source_id": "repo_source",
            "title": "Repo Source",
            "public_url": "https://example.edu/repo",
            "recommended_ingestion_method": "clone repo",
            "normalized_ingestion_method": "git_repo",
            "decision": "ingest",
        }
    )

    assert "license_review_pending" in source_skip_reasons(bash)
    assert "license_review_pending" not in source_skip_reasons(
        bash,
        allow_license_pending=True,
    )
    assert source_skip_reasons(missing_repo, allow_license_pending=True) == ["repo_url_required"]


def test_dry_run_writes_reports_without_fetching(tmp_path: Path) -> None:
    report = import_sources(
        ImportOptions(
            manifest_path=CONFIG_PATH,
            group="hpc_additional_docs_first_pass",
            report_dir=tmp_path / "reports",
            dry_run=True,
            ingest=False,
            run_id="dry-run",
        )
    )

    assert report.summary["sources_imported"] == 0
    assert report.summary["sources_skipped"] == 15
    assert (tmp_path / "reports" / "dry-run" / "summary.json").exists()
    assert (tmp_path / "reports" / "dry-run" / "sources_skipped.jsonl").exists()
