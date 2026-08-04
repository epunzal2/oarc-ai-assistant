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
    r"ood|mfa|vpn|license|licensed|data policy|quota|quotas|purge|backup|"
    r"login nodes?|compute nodes?|interactive jobs?)\b",
    re.IGNORECASE,
)
SLURM_BEHAVIOR_RE = re.compile(
    r"\b(slurm|sbatch|srun|salloc|scancel|squeue|sacct|scontrol|qos|gres|partition)\b",
    re.IGNORECASE,
)
EXPLICIT_EXAMPLE_RE = re.compile(
    r"\b(example|examples|other centers?|nersc|yale|princeton)\b|"
    r"\bexternal\s+(?:example|examples|center|centers|hpc|cluster|site|docs|documentation)\b",
    re.IGNORECASE,
)
LOCAL_GUIDE_FALLBACK_RE = re.compile(
    r"/scratch|"
    r"\b(login nodes?|compute nodes?|interactive jobs?|quick interactive|quick command|"
    r"heavy computations?|research applications?|external collaborators?|guest netid|"
    r"guest members?|open ondemand|ood|web browser|scratch storage|job arrays?|"
    r"general-access|general access|owned resources?|private job partitions?)\b",
    re.IGNORECASE,
)
FORCE_LOCAL_GUIDE_FALLBACK_RE = re.compile(
    r"/scratch|"
    r"\b(external collaborators?|guest netid|guest members?|open ondemand|ood|web browser|"
    r"scratch storage|job arrays?|general-access|general access|owned resources?|"
    r"private job partitions?)\b",
    re.IGNORECASE,
)


def is_local_operational_query(query: str) -> bool:
    """Return whether a query asks for local operational facts or policy."""

    return bool(LOCAL_OPERATIONAL_RE.search(str(query or "")))


def is_slurm_behavior_query(query: str) -> bool:
    """Return whether a query asks about Slurm syntax or behavior."""

    return bool(SLURM_BEHAVIOR_RE.search(str(query or "")))


def explicitly_allows_external_examples(query: str) -> bool:
    """Return whether a query explicitly asks for external examples."""

    return bool(EXPLICIT_EXAMPLE_RE.search(str(query or "")))


def needs_local_guide_fallback(query: str) -> bool:
    """Return whether a vector result should be augmented with local guide chunks."""

    text = str(query or "")
    return bool(
        LOCAL_GUIDE_FALLBACK_RE.search(text)
        and is_local_operational_query(text)
        and not explicitly_allows_external_examples(text)
    )


def forces_local_guide_fallback(query: str) -> bool:
    """Return whether local guide enrichment should run even when local docs are present."""

    return bool(FORCE_LOCAL_GUIDE_FALLBACK_RE.search(str(query or "")))


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


@dataclass(eq=False)
class LocalGuideFallbackRetriever:
    """Add local guide evidence for local-policy questions that vector recall misses."""

    retriever: Any
    fallback_retriever: Any
    final_top_k: int = 4
    last_retrieval_diagnostics: dict[str, Any] | None = None
    applies_source_policy: bool = True

    def invoke(self, query: str) -> list[Any]:
        primary_docs = _invoke_retriever(self.retriever, query)
        fallback_docs: list[Any] = []
        fallback_error: str | None = None

        fallback_needed = needs_local_guide_fallback(query) and (
            forces_local_guide_fallback(query) or not _has_local_doc(primary_docs)
        )
        if fallback_needed:
            try:
                fallback_docs = [
                    doc for doc in _invoke_retriever(self.fallback_retriever, query) if _is_local_doc(doc)
                ]
            except Exception as exc:  # pragma: no cover - defensive degradation path
                fallback_error = str(exc)[:200]

        merged_docs = _dedupe_documents([*fallback_docs, *primary_docs])
        final_docs = prioritize_documents(merged_docs, query)
        if self.final_top_k > 0:
            final_docs = final_docs[: self.final_top_k]

        diagnostics = getattr(self.retriever, "last_retrieval_diagnostics", None)
        self.last_retrieval_diagnostics = (
            dict(diagnostics) if isinstance(diagnostics, dict) else {}
        )
        self.last_retrieval_diagnostics.update(
            {
                "primary_count": len(primary_docs),
                "local_fallback_needed": fallback_needed,
                "local_fallback_count": len(fallback_docs),
                "local_fallback_error": fallback_error,
                "final_count": len(final_docs),
                "final_source_ids": [_source_id_for_doc(doc) for doc in final_docs],
            }
        )
        return final_docs

    def get_relevant_documents(self, query: str) -> list[Any]:
        return self.invoke(query)

    def __call__(self, query: str) -> list[Any]:
        return self.invoke(query)


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


@dataclass(eq=False)
class SourcePriorityRetriever:
    """Retriever wrapper that applies authority policy after base retrieval."""

    retriever: Any
    last_retrieval_diagnostics: dict[str, Any] | None = None

    def invoke(self, query: str) -> list[Any]:
        docs = _invoke_retriever(self.retriever, query)
        final_docs = prioritize_documents(docs, query)
        diagnostics = getattr(self.retriever, "last_retrieval_diagnostics", None)
        self.last_retrieval_diagnostics = (
            dict(diagnostics) if isinstance(diagnostics, dict) else {}
        )
        self.last_retrieval_diagnostics.update(
            {
                "final_count": len(final_docs),
                "final_source_ids": [_source_id_for_doc(doc) for doc in final_docs],
            }
        )
        return final_docs

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
    if getattr(retriever, "applies_source_policy", False):
        return retriever
    return SourcePriorityRetriever(retriever)


def _invoke_retriever(retriever: Any, query: str) -> list[Any]:
    if hasattr(retriever, "invoke"):
        return list(retriever.invoke(query))
    if hasattr(retriever, "get_relevant_documents"):
        return list(retriever.get_relevant_documents(query))
    return list(retriever(query))


def _source_id_for_doc(doc: Any) -> str:
    metadata = getattr(doc, "metadata", {}) or {}
    for key in ("chunk_id", "id", "document_id", "source", "content_hash"):
        value = metadata.get(key)
        if value:
            return str(value)
    page_content = getattr(doc, "page_content", "") or ""
    return str(page_content)[:80]


def _has_local_doc(docs: Iterable[Any]) -> bool:
    return any(_is_local_doc(doc) for doc in docs)


def _is_local_doc(doc: Any) -> bool:
    metadata = getattr(doc, "metadata", {}) or {}
    return (
        metadata.get("source_id") == "local_university_hpc_guide"
        or metadata.get("source_group") == "local"
    )


def _dedupe_documents(docs: Iterable[Any]) -> list[Any]:
    seen: set[str] = set()
    unique_docs: list[Any] = []
    for doc in docs:
        identity = _source_id_for_doc(doc)
        if identity in seen:
            continue
        seen.add(identity)
        unique_docs.append(doc)
    return unique_docs


__all__ = [
    "LocalGuideFallbackRetriever",
    "SourcePriorityRetriever",
    "explicitly_allows_external_examples",
    "forces_local_guide_fallback",
    "is_local_operational_query",
    "is_slurm_behavior_query",
    "maybe_wrap_retriever",
    "needs_local_guide_fallback",
    "prioritize_documents",
]
