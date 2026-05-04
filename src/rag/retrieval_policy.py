"""Authority-aware retrieval post-processing for mixed HPC corpora."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Iterable


LOCAL_OPERATIONAL_RE = re.compile(
    r"\b(local|amarel|rutgers|oarc|path|paths|scratch|home|project|projects|/work|"
    r"queue|queues|partition|partitions|qos|account|accounts|allocation|fairshare|"
    r"module|modules|software version|support|helpdesk|globus collection|open ondemand|"
    r"ood|mfa|vpn|license|licensed|data policy|quota|quotas|purge|backup)\b",
    re.IGNORECASE,
)
SLURM_BEHAVIOR_RE = re.compile(
    r"\b(slurm|sbatch|srun|salloc|scancel|squeue|sacct|scontrol|qos|gres|partition)\b",
    re.IGNORECASE,
)
EXPLICIT_EXAMPLE_RE = re.compile(r"\b(example|examples|external|other centers?|nersc|yale|princeton)\b", re.IGNORECASE)


def is_local_operational_query(query: str) -> bool:
    """Return whether a query asks for local operational facts or policy."""

    return bool(LOCAL_OPERATIONAL_RE.search(str(query or "")))


def is_slurm_behavior_query(query: str) -> bool:
    """Return whether a query asks about Slurm syntax or behavior."""

    return bool(SLURM_BEHAVIOR_RE.search(str(query or "")))


def explicitly_allows_external_examples(query: str) -> bool:
    """Return whether a query explicitly asks for external examples."""

    return bool(EXPLICIT_EXAMPLE_RE.search(str(query or "")))


def prioritize_documents(docs: Iterable[Any], query: str) -> list[Any]:
    """Filter and sort retrieved documents using source authority metadata."""

    doc_list = list(docs)
    local_query = is_local_operational_query(query)
    slurm_query = is_slurm_behavior_query(query)
    allow_external = explicitly_allows_external_examples(query)
    scored: list[tuple[float, int, Any]] = []

    for index, doc in enumerate(doc_list):
        metadata = getattr(doc, "metadata", {}) or {}
        source_group = str(metadata.get("source_group") or "")
        if (
            local_query
            and source_group == "external_hpc"
            and not allow_external
        ):
            continue

        score = _authority_score(metadata, local_query=local_query, slurm_query=slurm_query)
        scored.append((score, index, doc))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [doc for _, _, doc in scored]


def _authority_score(metadata: dict[str, Any], *, local_query: bool, slurm_query: bool) -> float:
    source_id = str(metadata.get("source_id") or "")
    source_group = str(metadata.get("source_group") or "")
    trust_tier = str(metadata.get("trust_tier") or "")
    try:
        retrieval_weight = float(metadata.get("retrieval_weight") or 1.0)
    except (TypeError, ValueError):
        retrieval_weight = 1.0

    score = retrieval_weight * 10.0
    if source_id == "local_university_hpc_guide" or source_group == "local":
        score += 300.0 if local_query else 180.0
    elif source_id == "slurm_documentation":
        score += 260.0 if slurm_query else 150.0
    elif source_group in {"official", "reference"} or trust_tier == "Tier 1":
        score += 210.0
    elif source_group == "external_hpc":
        score += 40.0
        if metadata.get("example_only"):
            score -= 20.0
        if metadata.get("cluster_specific"):
            score -= 15.0
    else:
        score += 80.0

    if metadata.get("local_conflict_risk") == "high":
        score -= 5.0
    return score


@dataclass
class SourcePriorityRetriever:
    """Retriever wrapper that applies authority policy after base retrieval."""

    retriever: Any

    def invoke(self, query: str) -> list[Any]:
        docs = _invoke_retriever(self.retriever, query)
        return prioritize_documents(docs, query)

    def get_relevant_documents(self, query: str) -> list[Any]:
        return self.invoke(query)

    def __call__(self, query: str) -> list[Any]:
        return self.invoke(query)


def maybe_wrap_retriever(retriever: Any) -> Any:
    """Wrap a retriever unless source-priority policy is disabled."""

    enabled = os.environ.get("RAG_SOURCE_POLICY_ENABLED", "true").strip().lower()
    if enabled in {"0", "false", "no", "off"}:
        return retriever
    if isinstance(retriever, SourcePriorityRetriever):
        return retriever
    return SourcePriorityRetriever(retriever)


def _invoke_retriever(retriever: Any, query: str) -> list[Any]:
    if hasattr(retriever, "invoke"):
        return list(retriever.invoke(query))
    if hasattr(retriever, "get_relevant_documents"):
        return list(retriever.get_relevant_documents(query))
    return list(retriever(query))


__all__ = [
    "SourcePriorityRetriever",
    "explicitly_allows_external_examples",
    "is_local_operational_query",
    "is_slurm_behavior_query",
    "maybe_wrap_retriever",
    "prioritize_documents",
]
