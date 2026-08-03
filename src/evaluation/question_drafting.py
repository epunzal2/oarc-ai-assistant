"""Draft acceptance-question candidates from approved Markdown corpus roots.

The drafter is deterministic and offline. It does not call an LLM or read raw
ServiceNow exports; generated rows are candidates that can be reviewed before
being promoted into the main acceptance JSONL.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence

DEFAULT_EXISTING_QUESTIONS = Path("data/evaluation/acceptance/rag_v1_questions.jsonl")
DEFAULT_OUTPUT_PATH = Path("data/evaluation/acceptance/rag_v1_candidate_questions.jsonl")
DEFAULT_SOURCE_PATHS = (
    Path("docs/google_sites_guide"),
    Path("docs/corpus/authoritative/rutgers/research-data-finder.md"),
    Path("docs/slurm-23.02.7/markdown/html"),
    Path("docs/slurm-23.02.7/markdown/man"),
)
BLOCKED_SOURCE_PATTERNS = (
    ".env",
    ".env.*",
    "**/.env",
    "**/.env.*",
    "docs/servicenow",
    "docs/servicenow/**",
    "docs/servicenow/task*.json",
    "docs/servicenow/task*.jsonl",
)
LOW_VALUE_SOURCE_PATTERNS = (
    "docs/corpus/authoritative/rutgers/oarc-website/crawl-report.md",
    "docs/corpus/authoritative/rutgers/oarc-website/events/**",
)
LOW_VALUE_HEADINGS = {
    "authors",
    "comparison field labels",
    "contents",
    "copying",
    "counts",
    "finder behavior",
    "files",
    "page content",
    "provenance",
    "see also",
    "summary",
}
COMMAND_TERMS = (
    "sbatch",
    "squeue",
    "scancel",
    "sacct",
    "sinfo",
    "srun",
    "module avail",
    "module load",
    "ssh",
    "scp",
    "rsync",
    "globus",
)
TOPIC_TERMS = (
    "/home",
    "/projects",
    "scratch",
    "allocation",
    "helpdesk",
    "support",
    "ticket",
    "duo",
    "vpn",
    "ood",
    "ondemand",
    "research data",
    "lab services",
    "amarel",
    "slurm",
)
STOP_WORDS = {
    "about",
    "after",
    "also",
    "amarel",
    "and",
    "are",
    "available",
    "before",
    "between",
    "can",
    "data",
    "does",
    "for",
    "from",
    "guide",
    "how",
    "into",
    "job",
    "more",
    "new",
    "not",
    "oarc",
    "research",
    "rutgers",
    "should",
    "slurm",
    "the",
    "this",
    "through",
    "use",
    "user",
    "using",
    "what",
    "when",
    "where",
    "with",
}


@dataclass(frozen=True)
class SourceSegment:
    """One heading-scoped Markdown segment used for candidate generation."""

    source_path: str
    heading: str
    text: str


def build_parser() -> argparse.ArgumentParser:
    """Create the question-drafting CLI parser."""

    parser = argparse.ArgumentParser(
        description="Draft deterministic RAG acceptance-question candidates from Markdown corpus."
    )
    parser.add_argument(
        "--source",
        type=Path,
        action="append",
        dest="sources",
        help="Approved Markdown corpus root. Repeat to include multiple roots.",
    )
    parser.add_argument(
        "--existing",
        type=Path,
        default=DEFAULT_EXISTING_QUESTIONS,
        help=f"Existing accepted JSONL questions to dedupe against ({DEFAULT_EXISTING_QUESTIONS}).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Candidate JSONL output path ({DEFAULT_OUTPUT_PATH}).",
    )
    parser.add_argument("--max-questions", type=int, default=24)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point used by `scripts/evaluation/draft_acceptance_questions.py`."""

    args = build_parser().parse_args(argv)
    repo_root = Path.cwd().resolve()
    sources = tuple(args.sources or DEFAULT_SOURCE_PATHS)
    candidates = draft_acceptance_questions(
        repo_root=repo_root,
        source_paths=sources,
        existing_questions_path=args.existing,
        max_questions=args.max_questions,
    )
    write_jsonl(args.output, candidates)
    print(f"wrote {len(candidates)} candidate question(s) to {args.output}")
    return 0


def draft_acceptance_questions(
    *,
    repo_root: Path,
    source_paths: Sequence[Path],
    existing_questions_path: Path | None = DEFAULT_EXISTING_QUESTIONS,
    max_questions: int = 24,
) -> list[dict[str, Any]]:
    """Return deterministic acceptance-question candidates from Markdown sources."""

    existing = load_existing_questions(existing_questions_path) if existing_questions_path else set()
    candidates: list[dict[str, Any]] = []
    used_ids = set(existing)
    used_questions = set(existing)

    segments = sorted(iter_source_segments(repo_root, source_paths), key=segment_score, reverse=True)
    for segment in segments:
        record = candidate_from_segment(segment)
        if record is None:
            continue
        question_key = normalize_text(record["question"])
        if record["id"] in used_ids or question_key in used_questions:
            continue
        record["id"] = unique_id(record["id"], used_ids)
        candidates.append(record)
        used_ids.add(record["id"])
        used_questions.add(question_key)
        if len(candidates) >= max_questions:
            break
    return candidates


def load_existing_questions(path: Path) -> set[str]:
    """Load existing IDs and question text for candidate dedupe."""

    if not path.exists():
        return set()
    values: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL") from exc
            for key in ("id", "question"):
                value = record.get(key)
                if isinstance(value, str) and value:
                    values.add(normalize_text(value))
    return values


def iter_source_segments(repo_root: Path, source_paths: Sequence[Path]) -> Iterable[SourceSegment]:
    """Yield heading-scoped segments from approved Markdown roots."""

    for path in iter_markdown_files(repo_root, source_paths):
        rel_path = path.relative_to(repo_root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for heading, body in split_markdown_segments(text):
            cleaned = clean_text(body)
            if len(cleaned) < 160:
                continue
            yield SourceSegment(source_path=rel_path, heading=heading, text=cleaned)


def iter_markdown_files(repo_root: Path, source_paths: Sequence[Path]) -> list[Path]:
    """Return sorted Markdown files under approved source roots."""

    files: list[Path] = []
    for raw_path in source_paths:
        root = raw_path if raw_path.is_absolute() else repo_root / raw_path
        root = root.resolve()
        try:
            rel_root = root.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError(f"source path must stay under repo root: {root}") from exc
        if _is_blocked(rel_root.as_posix()):
            raise ValueError(f"source path is blocked: {rel_root.as_posix()}")
        if root.is_file():
            candidates = [root]
        elif root.exists():
            candidates = sorted(
                path for path in root.rglob("*") if path.suffix.lower() in {".md", ".markdown"}
            )
        else:
            candidates = []
        for path in candidates:
            rel = path.relative_to(repo_root).as_posix()
            if _is_blocked(rel) or _is_low_value(rel):
                continue
            files.append(path)
    return sorted(set(files))


def split_markdown_segments(text: str) -> list[tuple[str, str]]:
    """Split Markdown into simple heading/body segments."""

    segments: list[tuple[str, str]] = []
    current_heading = "overview"
    current_lines: list[str] = []
    for line in text.splitlines():
        heading_match = re.match(r"^\s{0,3}#{1,4}\s+(.+?)\s*$", line)
        plain_heading = _looks_like_plain_heading(line)
        if heading_match or plain_heading:
            if current_lines:
                segments.append((current_heading, "\n".join(current_lines)))
                current_lines = []
            raw_heading = heading_match.group(1) if heading_match else line
            current_heading = clean_text(raw_heading)[:120] or "overview"
            continue
        current_lines.append(line)
    if current_lines:
        segments.append((current_heading, "\n".join(current_lines)))
    return segments


def candidate_from_segment(segment: SourceSegment) -> dict[str, Any] | None:
    """Build one acceptance candidate from a source segment."""

    if _is_low_value_heading(segment.heading):
        return None
    terms = infer_expected_terms(segment)
    if len(terms) < 2:
        return None
    category = infer_category(segment)
    source_hint = infer_source_hint(segment)
    question = build_question(category, terms, segment.heading)
    expected_topics = tuple(dict.fromkeys((*terms[:3], *_important_words(segment.heading, limit=2))))
    required_terms = tuple(term for term in terms if term in COMMAND_TERMS)[:1]
    slug = slugify(f"{category}-{segment.heading}-{terms[0]}")
    return {
        "id": slug[:80],
        "category": category,
        "question": question,
        "expected_topics": list(expected_topics[:5]),
        "expected_source_hint": source_hint,
        "required_answer_terms": list(required_terms),
        "source_path": segment.source_path,
        "source_heading": segment.heading,
        "reference_answer_excerpt": excerpt(segment.text),
    }


def infer_expected_terms(segment: SourceSegment) -> tuple[str, ...]:
    """Infer lightweight expected answer terms from segment text and heading."""

    lowered = f"{segment.heading}\n{segment.text}".lower()
    terms: list[str] = []
    for term in (*COMMAND_TERMS, *TOPIC_TERMS):
        if term in lowered:
            terms.append(term)
    terms.extend(_important_words(segment.heading, limit=4))
    terms.extend(_important_words(segment.text, limit=4))
    return tuple(dict.fromkeys(terms))[:6]


def infer_category(segment: SourceSegment) -> str:
    """Infer an acceptance category compatible with the current question set."""

    blob = f"{segment.source_path}\n{segment.heading}\n{segment.text}".lower()
    if "research-data-finder" in segment.source_path:
        return "research_data_services"
    if "slurm" in blob or any(term in blob for term in COMMAND_TERMS[:6]):
        return "slurm_basics"
    if any(term in blob for term in ("helpdesk", "support", "ticket", "allocation")):
        return "support_policy"
    if "research data" in blob or "lab services" in blob:
        return "research_data_services"
    return "amarel_access"


def infer_source_hint(segment: SourceSegment) -> str:
    """Infer the source hint checked against returned RAG source metadata."""

    blob = f"{segment.source_path}\n{segment.heading}\n{segment.text}".lower()
    if "research-data-finder" in segment.source_path:
        return "research data"
    if "slurm" in blob:
        return "slurm"
    if "research data" in blob:
        return "research data"
    if any(term in blob for term in ("helpdesk", "support", "ticket")):
        return "support"
    if any(term in blob for term in ("module", "software")):
        return "module"
    if any(term in blob for term in ("scp", "rsync", "globus", "transfer")):
        return "transfer"
    if any(term in blob for term in ("scratch", "/home", "/projects", "storage")):
        return "storage"
    return "amarel"


def build_question(category: str, terms: Sequence[str], heading: str) -> str:
    """Build a natural-language question from inferred terms."""

    term_set = set(terms)
    heading_lower = heading.lower()
    if category == "research_data_services":
        if "classification" in heading_lower:
            return (
                "Which Rutgers research data services should I consider for low-, "
                "moderate-, or high-risk data?"
            )
        if "gb" in heading_lower or "tb" in heading_lower:
            return f"Which Rutgers services fit {sentence_fragment(heading)} storage needs?"
        if heading_lower.endswith(")") and "(" in heading_lower:
            return f"Which services match the {sentence_fragment(heading)} filter?"
        return f"What does the Research Data Finder say about {sentence_fragment(heading)}?"
    if "sbatch" in term_set:
        return "What should I include when submitting a Slurm batch job with sbatch?"
    if "squeue" in term_set:
        return "How do I check queued or running Slurm jobs with squeue?"
    if "scancel" in term_set:
        return "How do I cancel a Slurm job with scancel?"
    if "sacct" in term_set:
        return "How can I inspect a completed or failed Slurm job with sacct?"
    if "sinfo" in term_set:
        return "How can I check why Slurm nodes are offline with sinfo?"
    if "srun" in term_set:
        return "When should I use srun for an interactive or quick Slurm command?"
    if "module load" in term_set:
        return "How do I load software modules on Amarel?"
    if "module avail" in term_set:
        return "How do I find available software modules on Amarel?"
    if {"scp", "rsync", "globus"} & term_set:
        return "How can I copy files between my computer and Amarel?"
    if "ssh" in term_set:
        return "How do I connect to Amarel over SSH?"
    if "allocation" in term_set:
        return "What should a research group know before requesting more compute resources?"
    if {"helpdesk", "support", "ticket"} & term_set:
        return "Where should I go for help with this OARC or Amarel issue?"
    if category == "research_data_services":
        return f"What should I know about {sentence_fragment(heading)}?"
    return f"What should I know about {sentence_fragment(heading)} on Amarel?"


def write_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    """Write records as sorted-key JSONL."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def unique_id(base: str, used: set[str]) -> str:
    """Return an ID not already present in `used`."""

    candidate = base
    suffix = 2
    while normalize_text(candidate) in used or candidate in used:
        candidate = f"{base[:72]}-{suffix}"
        suffix += 1
    return candidate


def normalize_text(value: str) -> str:
    """Normalize strings for stable dedupe."""

    return re.sub(r"\s+", " ", value.strip().lower())


def clean_text(value: str) -> str:
    """Remove common Markdown punctuation while preserving command/path terms."""

    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"^\s*[-*+]\s+", "", value, flags=re.MULTILINE)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def excerpt(value: str, *, max_chars: int = 700) -> str:
    """Return a compact reference excerpt for human review."""

    cleaned = clean_text(value)
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 3].rstrip() + "..."


def sentence_fragment(value: str) -> str:
    """Return a heading fragment suitable for a generated question."""

    fragment = clean_text(value).strip(" .:;-")
    return fragment[:80] if fragment else "this topic"


def slugify(value: str) -> str:
    """Return a stable lowercase identifier."""

    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "draft_question"


def _important_words(text: str, *, limit: int) -> tuple[str, ...]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_/-]{2,}", text.lower())
    selected: list[str] = []
    for word in words:
        if word in STOP_WORDS or word.isdigit():
            continue
        selected.append(word)
        if len(selected) >= limit:
            break
    return tuple(selected)


def _looks_like_plain_heading(line: str) -> bool:
    stripped = clean_text(line)
    if not stripped or len(stripped) > 90:
        return False
    if re.search(r"[.!?;,]$", stripped):
        return False
    if re.search(r"^\S+@\S+$|^https?://|^\[|^\(|^\$", stripped, flags=re.IGNORECASE):
        return False
    if re.search(r"\b(?:command not found|error|warning)\b", stripped, flags=re.IGNORECASE):
        return False
    words = re.findall(r"[A-Za-z0-9_/.-]+", stripped)
    if not words or len(words) > 10:
        return False
    return any(re.search(r"[A-Za-z]", word) for word in words)


def segment_score(segment: SourceSegment) -> int:
    """Rank segments so generated candidates prefer operational corpus facts."""

    blob = f"{segment.source_path}\n{segment.heading}\n{segment.text}".lower()
    score = 0
    for term in COMMAND_TERMS:
        if term in blob:
            score += 10
    for term in TOPIC_TERMS:
        if term in blob:
            score += 3
    if "docs/google_sites_guide" in segment.source_path:
        score += 8
    if "research-data-finder" in segment.source_path:
        score += 6
    if "docs/slurm-23.02.7/markdown/man" in segment.source_path:
        score += 5
    if "docs/slurm-23.02.7/markdown/html" in segment.source_path:
        score += 3
    if segment.heading.lower() == "overview":
        score -= 4
    if _is_low_value_heading(segment.heading):
        score -= 100
    return score


def _is_blocked(path: str) -> bool:
    normalized = str(PurePosixPath(path))
    return any(fnmatch(normalized, pattern) or fnmatch(f"./{normalized}", pattern) for pattern in BLOCKED_SOURCE_PATTERNS)


def _is_low_value(path: str) -> bool:
    normalized = str(PurePosixPath(path))
    return any(
        fnmatch(normalized, pattern) or fnmatch(f"./{normalized}", pattern)
        for pattern in LOW_VALUE_SOURCE_PATTERNS
    )


def _is_low_value_heading(heading: str) -> bool:
    normalized = normalize_text(re.sub(r"\([^)]*\)", "", heading)).strip(" :;-")
    if normalized in LOW_VALUE_HEADINGS:
        return True
    return bool(re.match(r"https?://", heading.strip(), flags=re.IGNORECASE))


if __name__ == "__main__":
    raise SystemExit(main())
