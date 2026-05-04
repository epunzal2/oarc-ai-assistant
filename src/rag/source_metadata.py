"""Metadata enrichment and cluster-specific detection for RAG corpus sources."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from src.rag.source_manifest import SourceRecord


ABSOLUTE_PATH_RE = re.compile(
    r"(?<![\w.-])/(scratch|home|project|projects|work|global|gpfs|glade|ocean|lustre|nfs)"
    r"(?:/[A-Za-z0-9._~+@%=-]+)*"
)
SCHEDULING_RE = re.compile(
    r"\b(queue|queues|partition|partitions|qos|account|allocation|fairshare|"
    r"--partition|--qos|--account|SBATCH\s+-[A-Z]*p|SBATCH\s+--gres)\b",
    re.IGNORECASE,
)
MODULE_RE = re.compile(
    r"\bmodule\s+(?:load|add|use)\s+\S+/\S+|"
    r"\b(?:cuda|gcc|openmpi|mvapich|intel|python|r)/\d+(?:\.\d+)+",
    re.IGNORECASE,
)
HOSTNAME_RE = re.compile(
    r"\b(?:login|dtn|ood|ondemand|globus|vpn)[A-Za-z0-9.-]*\.[A-Za-z]{2,}\b",
    re.IGNORECASE,
)
SUPPORT_RE = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|"
    r"\b(?:helpdesk|ticket|service desk)\b|https?://\S*(?:ticket|support|helpdesk)\S*",
    re.IGNORECASE,
)
QUOTA_RE = re.compile(
    r"\b(quota|quotas|purge|purged|backup|backups|billing|charging|pi account|"
    r"project account|allocation policy)\b",
    re.IGNORECASE,
)
ACCESS_POLICY_RE = re.compile(r"\b(mfa|vpn|duo|two-factor|2fa|sso|bastion)\b", re.IGNORECASE)
DATA_POLICY_RE = re.compile(
    r"\b(sensitive data|data classification|hipaa|phi|ferpa|controlled data)\b",
    re.IGNORECASE,
)


DETECTORS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("paths", ABSOLUTE_PATH_RE),
    ("scheduling", SCHEDULING_RE),
    ("modules", MODULE_RE),
    ("hostnames", HOSTNAME_RE),
    ("support", SUPPORT_RE),
    ("quotas", QUOTA_RE),
    ("access_policy", ACCESS_POLICY_RE),
    ("data_policy", DATA_POLICY_RE),
)


def detect_cluster_specific_fields(text: str) -> list[str]:
    """Return cluster-specific field categories detected in text."""

    body = str(text or "")
    fields = []
    for name, pattern in DETECTORS:
        match = pattern.search(body)
        if not match:
            continue
        if name == "support" and not _is_support_contact_match(body, match):
            continue
        fields.append(name)
    return fields


def _is_support_contact_match(text: str, match: re.Match[str]) -> bool:
    matched = match.group(0)
    if "@" not in matched:
        return True
    window = text[max(0, match.start() - 80) : match.end() + 80]
    return bool(re.search(r"\b(contact|support|helpdesk|ticket|email|write to)\b", window, re.IGNORECASE))


def stable_content_hash(text: str) -> str:
    """Return a short stable hash for normalized content."""

    normalized = "\n".join(line.rstrip() for line in str(text or "").splitlines()).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def metadata_for_source(
    source: SourceRecord,
    *,
    canonical_url: str | None = None,
    content: str = "",
    path_or_heading: str = "",
) -> dict[str, Any]:
    """Build chunk/document metadata inherited from a source manifest record."""

    fields = detect_cluster_specific_fields(content)
    example_only = source.example_only_default
    if source.source_group == "external_hpc" and fields:
        example_only = True

    return {
        "source_id": source.source_id,
        "source_title": source.title,
        "title": source.title,
        "organization_or_maintainer": source.organization_or_maintainer,
        "canonical_url": canonical_url or source.public_url,
        "url": canonical_url or source.public_url,
        "source_group": source.source_group,
        "source_type": source.source_type,
        "trust_tier": source.trust_tier,
        "authority_scope": source.authority_scope,
        "topic_tags": source.tags,
        "local_conflict_risk": source.risk_of_conflicting_with_local_docs,
        "cluster_specific": bool(fields),
        "cluster_specific_fields_detected": fields,
        "example_only": example_only,
        "license_note": source.license_note,
        "retrieval_weight": source.retrieval_weight,
        "path_or_heading": path_or_heading,
        "content_hash": stable_content_hash(content),
    }


def infer_source_metadata_from_path(path: str | Path, *, content: str = "") -> dict[str, Any]:
    """Infer authority metadata for existing local and Slurm Markdown paths."""

    source_path = Path(path)
    normalized = source_path.as_posix()
    fields = detect_cluster_specific_fields(content)

    if "docs/google_sites_guide/" in normalized or normalized.startswith("docs/google_sites_guide/"):
        return {
            "source_id": "local_university_hpc_guide",
            "source_title": "Local university HPC guide",
            "title": source_path.stem.replace("_", " ").replace("-", " ").title(),
            "organization_or_maintainer": "Rutgers OARC",
            "canonical_url": normalized,
            "source_group": "local",
            "source_type": "local university HPC guide",
            "trust_tier": "Tier 0",
            "authority_scope": ["local_policy", "cluster_operations"],
            "topic_tags": ["amarel", "oarc", "local-hpc-guide"],
            "local_conflict_risk": "authoritative",
            "cluster_specific": True,
            "cluster_specific_fields_detected": sorted(set(fields) | {"local_policy"}),
            "example_only": False,
            "license_note": "Local OARC guide; internal corpus authority for Amarel policy.",
            "retrieval_weight": 1.3,
        }

    if "docs/slurm-23.02.7/markdown/" in normalized or normalized.startswith(
        "docs/slurm-23.02.7/markdown/"
    ):
        return {
            "source_id": "slurm_documentation",
            "source_title": "Slurm 23.02.7 documentation",
            "title": source_path.stem.replace("_", " ").replace("-", " ").title(),
            "organization_or_maintainer": "SchedMD",
            "canonical_url": normalized,
            "source_group": "reference",
            "source_type": "official Slurm documentation",
            "trust_tier": "Tier 1",
            "authority_scope": ["scheduler_behavior", "slurm_syntax"],
            "topic_tags": ["slurm", "scheduler"],
            "local_conflict_risk": "medium",
            "cluster_specific": bool(fields),
            "cluster_specific_fields_detected": fields,
            "example_only": False,
            "license_note": "Vendored official Slurm source documentation.",
            "retrieval_weight": 1.15,
        }

    return {
        "canonical_url": normalized,
        "cluster_specific": bool(fields),
        "cluster_specific_fields_detected": fields,
        "content_hash": stable_content_hash(content),
    }


def parse_metadata_sidecar(path: str | Path) -> dict[str, Any]:
    """Read optional JSON sidecar metadata next to a Markdown document."""

    source_path = Path(path)
    candidates = [
        source_path.with_suffix(source_path.suffix + ".metadata.json"),
        source_path.with_suffix(".metadata.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Split optional YAML front matter from Markdown content."""

    body = str(text or "")
    if not body.startswith("---\n"):
        return {}, body
    try:
        _, raw_metadata, content = body.split("---", 2)
    except ValueError:
        return {}, body

    metadata: dict[str, Any] = {}
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(raw_metadata) or {}
        if isinstance(loaded, dict):
            metadata = loaded
    except Exception:
        metadata = {}
    return metadata, content.lstrip("\n")


__all__ = [
    "detect_cluster_specific_fields",
    "infer_source_metadata_from_path",
    "metadata_for_source",
    "parse_metadata_sidecar",
    "split_front_matter",
    "stable_content_hash",
]
