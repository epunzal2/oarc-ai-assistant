"""Source manifest helpers for optional HPC documentation imports."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CONFIG_PATH = Path("configs/rag_sources/hpc_research_pro_sources.json")


@dataclass(frozen=True)
class SourceRecord:
    """One configured external or upstream documentation source."""

    source_id: str
    title: str
    organization_or_maintainer: str
    public_url: str
    source_group: str
    source_type: str
    trust_tier: str
    recommended_ingestion_method: str
    normalized_ingestion_method: str
    decision: str
    include_rules: list[str] = field(default_factory=list)
    exclude_rules: list[str] = field(default_factory=list)
    risk_of_conflicting_with_local_docs: str = "medium"
    tags: list[str] = field(default_factory=list)
    chunking_strategy: str = ""
    authority_scope: list[str] = field(default_factory=list)
    retrieval_weight: float = 1.0
    license_note: str = ""
    license_review_required: bool = False
    crawler_hints: dict[str, Any] = field(default_factory=dict)
    example_only_default: bool = False
    enabled_by_default: bool = False
    repo_url: str | None = None
    license_review_status: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceRecord":
        """Build a record from the repository source config."""

        return cls(
            source_id=str(payload["source_id"]),
            title=str(payload.get("title") or payload["source_id"]),
            organization_or_maintainer=str(payload.get("organization_or_maintainer") or ""),
            public_url=str(payload.get("public_url") or ""),
            source_group=str(payload.get("source_group") or ""),
            source_type=str(payload.get("source_type") or ""),
            trust_tier=str(payload.get("trust_tier") or ""),
            recommended_ingestion_method=str(payload.get("recommended_ingestion_method") or ""),
            normalized_ingestion_method=str(
                payload.get("normalized_ingestion_method")
                or normalize_ingestion_method(payload.get("recommended_ingestion_method", ""))
            ),
            decision=str(payload.get("decision") or ""),
            include_rules=[str(item) for item in payload.get("include_rules") or []],
            exclude_rules=[str(item) for item in payload.get("exclude_rules") or []],
            risk_of_conflicting_with_local_docs=str(
                payload.get("risk_of_conflicting_with_local_docs") or "medium"
            ),
            tags=[str(item) for item in payload.get("tags") or []],
            chunking_strategy=str(payload.get("chunking_strategy") or ""),
            authority_scope=[str(item) for item in payload.get("authority_scope") or []],
            retrieval_weight=float(payload.get("retrieval_weight") or 1.0),
            license_note=str(payload.get("license_note") or ""),
            license_review_required=bool(payload.get("license_review_required")),
            crawler_hints=dict(payload.get("crawler_hints") or {}),
            example_only_default=bool(payload.get("example_only_default")),
            enabled_by_default=bool(payload.get("enabled_by_default")),
            repo_url=payload.get("repo_url") or payload.get("clone_url"),
            license_review_status=payload.get("license_review_status"),
        )

    @property
    def license_review_approved(self) -> bool:
        """Return whether config explicitly marks reuse review as approved."""

        return str(self.license_review_status or "").lower() in {"approved", "cleared"}


@dataclass(frozen=True)
class SourceManifest:
    """Loaded Research Pro source configuration."""

    path: Path
    schema_version: str
    defaults: dict[str, Any]
    groups: dict[str, list[str]]
    sources: list[SourceRecord]
    source_priority: dict[str, str]
    retrieval_policy: dict[str, Any]

    @classmethod
    def from_file(cls, path: str | Path = CONFIG_PATH) -> "SourceManifest":
        """Read and validate a source manifest config file."""

        manifest_path = Path(path)
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        sources = [SourceRecord.from_dict(item) for item in payload.get("sources") or []]
        source_ids = {source.source_id for source in sources}
        groups = {
            str(name): [str(source_id) for source_id in source_ids_in_group]
            for name, source_ids_in_group in (payload.get("groups") or {}).items()
        }
        missing = sorted(
            source_id
            for group_ids in groups.values()
            for source_id in group_ids
            if source_id not in source_ids
        )
        if missing:
            raise ValueError(f"Source group references unknown source ids: {missing}")
        return cls(
            path=manifest_path,
            schema_version=str(payload.get("schema_version") or ""),
            defaults=dict(payload.get("defaults") or {}),
            groups=groups,
            sources=sources,
            source_priority=dict(payload.get("source_priority") or {}),
            retrieval_policy=dict(payload.get("retrieval_policy") or {}),
        )

    def source_by_id(self) -> dict[str, SourceRecord]:
        """Return configured sources keyed by source id."""

        return {source.source_id: source for source in self.sources}

    def resolve_group(self, group: str) -> list[SourceRecord]:
        """Resolve a named source group into ordered source records."""

        if group not in self.groups:
            raise KeyError(f"Unknown source group: {group}")
        by_id = self.source_by_id()
        return [by_id[source_id] for source_id in self.groups[group]]


def normalize_ingestion_method(method: str) -> str:
    """Map Research Pro ingestion methods to the local source-type names."""

    text = str(method or "").lower()
    if "review_manually_or_link_only" in text:
        return "skipped"
    if "manual export" in text or "review manually" in text:
        return "manual_review"
    if "link-only" in text or "link only" in text:
        return "citation_only"
    if "texinfo" in text or "download rendered static" in text or "download static" in text:
        return "static_manual"
    if "scrape" in text:
        return "controlled_website"
    if "clone" in text and "repo" in text:
        return "git_repo"
    if "download pdf" in text:
        return "manual_review"
    return "manual_review"


def source_skip_reasons(
    source: SourceRecord,
    *,
    allow_license_pending: bool = False,
) -> list[str]:
    """Return reasons this source should not be fetched by default."""

    reasons: list[str] = []
    decision = source.decision.lower()
    method = source.normalized_ingestion_method

    if "exclude" in decision:
        reasons.append("decision_exclude")
    if decision.startswith("review") or "review_manually" in decision:
        reasons.append("manual_review_required")
    if "link_only" in decision or method == "citation_only":
        reasons.append("link_only")
    if method in {"manual_review", "skipped"}:
        reasons.append(method)
    if (
        source.license_review_required
        and not allow_license_pending
        and not source.license_review_approved
    ):
        reasons.append("license_review_pending")
    if method == "git_repo" and not source.repo_url:
        reasons.append("repo_url_required")

    return sorted(set(reasons))


def selected_sources(
    manifest_path: str | Path,
    *,
    group: str,
) -> list[SourceRecord]:
    """Convenience wrapper for loading a manifest and resolving one group."""

    return SourceManifest.from_file(manifest_path).resolve_group(group)


__all__ = [
    "CONFIG_PATH",
    "SourceManifest",
    "SourceRecord",
    "normalize_ingestion_method",
    "selected_sources",
    "source_skip_reasons",
]
