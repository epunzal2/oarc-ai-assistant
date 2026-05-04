"""Tests for controlled optional source import behavior."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.rag.source_importer import ImportOptions, import_sources


class FakeResponse:
    """Small requests-like response fixture."""

    def __init__(self, text: str, *, status_code: int = 200, url: str = "https://example.edu/") -> None:
        self.text = text
        self.status_code = status_code
        self.url = url
        self.headers = {"content-type": "text/html"}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    """Requests-like session backed by an in-memory route map."""

    def __init__(self, routes: dict[str, FakeResponse]) -> None:
        self.routes = routes
        self.headers: dict[str, str] = {}
        self.requested: list[str] = []

    def get(self, url: str, timeout: int = 60) -> FakeResponse:
        self.requested.append(url)
        if url not in self.routes:
            return FakeResponse("", status_code=404, url=url)
        return self.routes[url]


def test_controlled_import_restricts_domain_rules_robots_and_page_caps(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path)
    routes = {
        "https://example.edu/robots.txt": FakeResponse("User-agent: *\nDisallow: /allowed/private\n"),
        "https://example.edu/start": FakeResponse(
            """
            <html><body><main><h1>Start</h1>
            <a href="/allowed/page">Allowed page</a>
            <a href="/allowed/private">Private page</a>
            <a href="/allowed/account">Account page</a>
            <a href="https://other.edu/allowed/page">Other domain</a>
            <a href="/allowed/skip">Skip page</a>
            </main></body></html>
            """,
            url="https://example.edu/start",
        ),
        "https://example.edu/allowed/page": FakeResponse(
            "<html><body><main><h1>Allowed</h1><pre>module load cuda/12.1</pre></main></body></html>",
            url="https://example.edu/allowed/page",
        ),
    }

    report = import_sources(
        ImportOptions(
            manifest_path=manifest_path,
            group="first",
            output_dir=tmp_path / "out",
            report_dir=tmp_path / "reports",
            ingest=True,
            dry_run=False,
            allow_license_pending=True,
            max_pages_per_source=5,
            request_timeout=5.0,
            run_id="crawl",
        ),
        session=FakeSession(routes),
    )

    skipped_reasons = {record["reason"] for record in report.pages_skipped}

    assert report.summary["sources_imported"] == 1
    assert report.sources_imported[0]["pages_imported"] == 2
    assert "robots_disallow" in skipped_reasons
    assert "default_cluster_policy_exclude" in skipped_reasons
    assert "different_domain" in skipped_reasons
    assert "exclude_rule" in skipped_reasons
    assert report.cluster_specific_pages
    assert list((tmp_path / "out").rglob("*.md"))


def _write_manifest(tmp_path: Path) -> Path:
    path = tmp_path / "manifest.json"
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "defaults": {
            "obey_robots_txt": True,
            "max_pages_per_source": 5,
            "output_root": str(tmp_path / "out"),
            "report_root": str(tmp_path / "reports"),
        },
        "groups": {"first": ["example_source"]},
        "sources": [
            {
                "source_id": "example_source",
                "title": "Example",
                "organization_or_maintainer": "Example",
                "public_url": "https://example.edu/start",
                "source_group": "official",
                "source_type": "official upstream docs",
                "trust_tier": "Tier 1",
                "recommended_ingestion_method": "scrape approved path prefix",
                "normalized_ingestion_method": "controlled_website",
                "decision": "ingest",
                "include_rules": ["/allowed"],
                "exclude_rules": ["skip"],
                "risk_of_conflicting_with_local_docs": "low",
                "tags": ["example"],
                "authority_scope": ["tool_behavior"],
                "retrieval_weight": 1.0,
                "license_note": "approved for test",
                "license_review_required": False,
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path
