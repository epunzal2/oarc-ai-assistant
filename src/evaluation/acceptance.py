"""Mac mini RAG v1 acceptance harness.

The harness calls the OpenAI-compatible RAG gateway with a curated, non-sensitive
golden question set and writes JSONL evidence suitable for promotion decisions.
It does not read raw ServiceNow exports or local private attachment files.
"""

from __future__ import annotations

import argparse
import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlparse

import requests

from src.evaluation.acceptance_report import (
    compare_acceptance_runs,
    print_comparison,
    write_acceptance_report,
)
from src.evaluation.gateway_eval import (
    DEFAULT_MAX_P95_LATENCY_MS,
    DEFAULT_MAX_P95_TTFT_MS,
    GatewayEvalThresholds,
    build_health_url,
    build_models_url,
    normalize_completions_url,
    post_chat_completion,
    source_summary,
    summarize_gateway_results,
)

DEFAULT_COMPLETIONS_URL = "http://127.0.0.1:18088/v1/chat/completions"
DEFAULT_QUESTIONS_PATH = Path("data/evaluation/acceptance/rag_v1_questions.jsonl")
DEFAULT_OUTPUT_DIR = Path("logs/rag_v1_acceptance")
DEFAULT_MODEL = "oarc-rag-v1"
DEFAULT_TIMEOUT = 120.0
ANSWER_EXCERPT_CHARS = 800
TOP_SOURCE_LIMIT = 3
ATTACHMENT_TOKEN_PATTERN = re.compile(r"OARC_ACCEPTANCE_[A-Z0-9_]+")
SYNTHETIC_ATTACHMENT_PHRASE_PATTERN = re.compile(
    r"synthetic acceptance note[^.]*\.",
    re.IGNORECASE,
)
SAFETY_SIGNAL_TERMS = (
    "cannot",
    "can't",
    "do not",
    "don't",
    "unable",
    "not provide",
    "not available",
    "contact",
    "helpdesk",
    "support",
    "administrator",
    "official",
)


@dataclass(frozen=True)
class AcceptanceQuestion:
    """One curated gateway acceptance prompt and its lightweight checks."""

    id: str
    category: str
    question: str
    expected_topics: tuple[str, ...] = ()
    expected_source_hint: str | None = None
    required_answer_terms: tuple[str, ...] = ()
    forbidden_answer_terms: tuple[str, ...] = ()
    requires_sources: bool = True
    safety: bool = False
    attachment: dict[str, Any] | None = None

    @property
    def uses_attachment(self) -> bool:
        return bool(self.attachment and self.attachment.get("enabled", True))


@dataclass(frozen=True)
class AcceptanceRunResult:
    """Paths and summary returned by a completed acceptance run."""

    run_dir: Path
    results_path: Path
    summary_path: Path
    summary: dict[str, Any]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the acceptance harness."""

    parser = argparse.ArgumentParser(
        description="Run the Mac mini RAG v1 acceptance question set.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_COMPLETIONS_URL,
        help=(
            "Gateway root, /v1 base, or /v1/chat/completions URL "
            f"(default: {DEFAULT_COMPLETIONS_URL})."
        ),
    )
    parser.add_argument(
        "--questions",
        type=Path,
        default=DEFAULT_QUESTIONS_PATH,
        help=f"Path to JSONL acceptance questions (default: {DEFAULT_QUESTIONS_PATH}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Base directory for ignored run outputs (default: {DEFAULT_OUTPUT_DIR}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds per gateway call (default: {DEFAULT_TIMEOUT}).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gateway model alias to send in requests (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--max-questions",
        type=int,
        default=None,
        help="Run only the first N questions from the curated set.",
    )
    parser.add_argument(
        "--stream",
        dest="stream",
        action="store_true",
        default=True,
        help="Use OpenAI-style streaming and record TTFT metrics. This is the default.",
    )
    parser.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        help="Use non-streaming completions. TTFT gate will fail unless thresholds are ignored downstream.",
    )
    parser.add_argument(
        "--max-p95-latency-ms",
        type=float,
        default=DEFAULT_MAX_P95_LATENCY_MS,
        help=(
            "Automated gate threshold for p95 end-to-end latency "
            f"(default: {DEFAULT_MAX_P95_LATENCY_MS})."
        ),
    )
    parser.add_argument(
        "--max-p95-ttft-ms",
        type=float,
        default=DEFAULT_MAX_P95_TTFT_MS,
        help=(
            "Automated gate threshold for p95 time to first token "
            f"(default: {DEFAULT_MAX_P95_TTFT_MS})."
        ),
    )
    parser.add_argument(
        "--no-full-answer",
        dest="include_full_answer",
        action="store_false",
        default=False,
        help="Store answer excerpts only. This is the default privacy posture.",
    )
    parser.add_argument(
        "--include-full-answer",
        dest="include_full_answer",
        action="store_true",
        help="Store full generated answers in JSONL evidence.",
    )
    parser.add_argument(
        "--compare-runs",
        nargs=2,
        metavar=("RUN_A", "RUN_B"),
        help=(
            "Compare two existing acceptance run directories or summary.json files. "
            "No gateway calls are made."
        ),
    )
    return parser.parse_args(argv)


def load_questions(path: Path, max_questions: int | None = None) -> list[AcceptanceQuestion]:
    """Load and validate the curated acceptance JSONL question set."""

    if max_questions is not None and max_questions < 1:
        raise ValueError("max_questions must be a positive integer")

    questions: list[AcceptanceQuestion] = []
    seen_ids: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}: {exc}") from exc
            question = _question_from_record(record, line_number=line_number)
            if question.id in seen_ids:
                raise ValueError(f"duplicate question id: {question.id}")
            seen_ids.add(question.id)
            questions.append(question)
            if max_questions is not None and len(questions) >= max_questions:
                break
    return questions


def run_acceptance(
    *,
    base_url: str,
    questions_path: Path,
    output_dir: Path,
    timeout: float,
    model: str,
    max_questions: int | None = None,
    include_full_answer: bool = False,
    stream: bool = True,
    thresholds: GatewayEvalThresholds | None = None,
    session: Any | None = None,
    run_timestamp: str | None = None,
) -> AcceptanceRunResult:
    """Run the curated question set and persist JSONL plus summary evidence."""

    completions_url = normalize_completions_url(base_url)
    health_url = build_health_url(completions_url)
    models_url = build_models_url(completions_url)
    http = session or requests.Session()
    questions = load_questions(questions_path, max_questions=max_questions)
    attachments_enabled, health = _fetch_attachment_capability(http, health_url, timeout)
    models = _fetch_models_capability(http, models_url, timeout)
    thresholds = thresholds or GatewayEvalThresholds()

    timestamp = run_timestamp or _run_timestamp()
    run_dir = output_dir / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    results_path = run_dir / "results.jsonl"
    summary_path = run_dir / "summary.json"
    report_path = run_dir / "report.md"

    records = [
        _run_one_question(
            question=question,
            session=http,
            completions_url=completions_url,
            timeout=timeout,
            model=model,
            attachments_enabled=attachments_enabled,
            include_full_answer=include_full_answer,
            stream=stream,
        )
        for question in questions
    ]
    summary = summarize_results(
        records,
        attachments_enabled=attachments_enabled,
        thresholds=thresholds,
    )
    summary.update(
        {
            "base_url": completions_url,
            "health_url": health_url,
            "models_url": models_url,
            "health": health,
            "models": models,
            "model": model,
            "questions_path": str(questions_path),
            "run_dir": str(run_dir),
            "results_path": str(results_path),
            "summary_path": str(summary_path),
            "report_path": str(report_path),
            "full_answers_included": include_full_answer,
            "stream": stream,
        }
    )
    summary.update(
        _run_metadata_from_gateway(
            completions_url=completions_url,
            health=health,
            models=models,
            max_questions=max_questions,
        )
    )
    _finalize_promotion_checklist(summary, max_questions=max_questions)

    _write_jsonl(results_path, records)
    write_acceptance_report(run_dir, summary, records)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return AcceptanceRunResult(
        run_dir=run_dir,
        results_path=results_path,
        summary_path=summary_path,
        summary=summary,
    )


def summarize_results(
    records: Sequence[dict[str, Any]],
    *,
    attachments_enabled: bool,
    thresholds: GatewayEvalThresholds | None = None,
) -> dict[str, Any]:
    """Aggregate acceptance records into promotion-gate summary metrics."""

    return summarize_gateway_results(
        records,
        attachments_enabled=attachments_enabled,
        thresholds=thresholds or GatewayEvalThresholds(),
    )


def print_summary(summary: dict[str, Any]) -> None:
    """Emit a compact human-readable summary for terminal runs."""

    print("Mac mini RAG v1 acceptance summary")
    print(f"Results: {summary.get('results_path')}")
    print(f"Summary: {summary.get('summary_path')}")
    print(f"Report: {summary.get('report_path')}")
    print(
        "Questions: "
        f"{summary['executed_questions']} executed / "
        f"{summary['skipped_questions']} skipped / "
        f"{summary['total_questions']} total"
    )
    print(f"Pass: {summary['pass_count']}  Fail: {summary['fail_count']}")
    print(
        "Latency: "
        f"p50={summary.get('p50_latency_ms')} ms  "
        f"p95={summary.get('p95_latency_ms')} ms"
    )
    print(
        "TTFT: "
        f"p50={summary.get('p50_time_to_first_token_ms')} ms  "
        f"p95={summary.get('p95_time_to_first_token_ms')} ms"
    )
    print(f"Attachments enabled: {summary.get('attachments_enabled')}")
    print(f"Promotion ready: {summary.get('promotion_ready')}")
    if summary.get("automated_gates"):
        print(f"Automated gates: {summary['automated_gates']}")
    if summary.get("failures_by_category"):
        print(f"Failures by category: {summary['failures_by_category']}")
    if summary.get("zero_source_question_ids"):
        print(f"Zero-source questions: {summary['zero_source_question_ids']}")
    if summary.get("manual_review_question_ids"):
        print(f"Manual review: {summary['manual_review_question_ids']}")
    if summary.get("skipped_question_ids"):
        print(f"Skipped: {summary['skipped_question_ids']}")


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for `scripts/evaluation/run_v1_acceptance.py`."""

    args = parse_args(argv)
    if args.compare_runs:
        comparison = compare_acceptance_runs(
            Path(args.compare_runs[0]),
            Path(args.compare_runs[1]),
            write_report=True,
        )
        print_comparison(comparison)
        return 0

    result = run_acceptance(
        base_url=args.base_url,
        questions_path=args.questions,
        output_dir=args.output_dir,
        timeout=args.timeout,
        model=args.model,
        max_questions=args.max_questions,
        include_full_answer=args.include_full_answer,
        stream=args.stream,
        thresholds=GatewayEvalThresholds(
            max_p95_latency_ms=args.max_p95_latency_ms,
            max_p95_ttft_ms=args.max_p95_ttft_ms,
        ),
    )
    print_summary(result.summary)
    return 0 if result.summary.get("promotion_ready") else 1


def _question_from_record(record: dict[str, Any], *, line_number: int) -> AcceptanceQuestion:
    if not isinstance(record, dict):
        raise ValueError(f"line {line_number}: question record must be an object")
    required = ("id", "category", "question")
    for field in required:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"line {line_number}: missing required field {field}")

    attachment = record.get("attachment")
    if attachment is not None and not isinstance(attachment, dict):
        raise ValueError(f"line {line_number}: attachment must be an object")
    safety = bool(record.get("safety", False))
    requires_sources = bool(
        record.get(
            "requires_sources",
            False if safety or attachment else True,
        )
    )
    expected_source_hint = record.get("expected_source_hint")
    if expected_source_hint is not None and not isinstance(expected_source_hint, str):
        raise ValueError(f"line {line_number}: expected_source_hint must be a string")

    return AcceptanceQuestion(
        id=record["id"].strip(),
        category=record["category"].strip(),
        question=record["question"].strip(),
        expected_topics=_string_tuple(record, "expected_topics", line_number=line_number),
        expected_source_hint=expected_source_hint,
        required_answer_terms=_string_tuple(
            record,
            "required_answer_terms",
            line_number=line_number,
        ),
        forbidden_answer_terms=_string_tuple(
            record,
            "forbidden_answer_terms",
            line_number=line_number,
        ),
        requires_sources=requires_sources,
        safety=safety,
        attachment=attachment,
    )


def _string_tuple(
    record: dict[str, Any],
    field: str,
    *,
    line_number: int,
) -> tuple[str, ...]:
    value = record.get(field, [])
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"line {line_number}: {field} must be a list of strings")
    return tuple(item.strip() for item in value if item.strip())


def _fetch_attachment_capability(
    session: Any,
    health_url: str,
    timeout: float,
) -> tuple[bool, dict[str, Any]]:
    try:
        response = session.get(health_url, timeout=timeout)
        payload = response.json()
    except Exception as exc:
        return False, {"status": "unknown", "error": _sanitize_error(exc)}

    enabled = bool(
        response.status_code < 400
        and isinstance(payload, dict)
        and isinstance(payload.get("ui"), dict)
        and payload["ui"].get("attachments_enabled") is True
    )
    health = dict(payload) if isinstance(payload, dict) else {}
    health.update(
        {
            "http_status": response.status_code,
            "attachments_enabled": enabled,
        }
    )
    if "status" not in health:
        health["status"] = payload.get("status") if isinstance(payload, dict) else None
    return enabled, health


def _fetch_models_capability(
    session: Any,
    models_url: str,
    timeout: float,
) -> dict[str, Any]:
    try:
        response = session.get(models_url, timeout=timeout)
        payload = response.json()
    except Exception as exc:
        return {"http_status": None, "status": "unknown", "error": _sanitize_error(exc)}
    return {
        "http_status": response.status_code,
        "status": "ok" if response.status_code < 400 else "degraded",
        "payload": payload if isinstance(payload, dict) else {},
    }


def _run_metadata_from_gateway(
    *,
    completions_url: str,
    health: dict[str, Any],
    models: dict[str, Any],
    max_questions: int | None,
) -> dict[str, Any]:
    backend = health.get("backend") if isinstance(health.get("backend"), dict) else {}
    model_metadata = _first_model_metadata(models)
    combined = {**model_metadata, **backend}
    vector_store_type = _optional_str(combined.get("vector_store_type"))
    faiss_index_path = _optional_str(combined.get("faiss_index_path"))
    retrieval_mode = _optional_str(combined.get("retrieval_mode"))
    health_passed = int(health.get("http_status") or 0) < 400 and health.get("status") == "ok"
    models_passed = int(models.get("http_status") or 0) < 400 and models.get("status") == "ok"
    attachments_enabled = bool(health.get("attachments_enabled"))
    is_loopback = _is_loopback_url(completions_url)

    metadata = {
        "backend_model": combined.get("backing_model"),
        "backend_provider": combined.get("backing_provider"),
        "vector_store_type": vector_store_type,
        "embedding_model": combined.get("embedding_model"),
        "faiss_index_path": faiss_index_path,
        "retrieval_mode": retrieval_mode or ("keyword" if vector_store_type == "keyword" else "vector"),
        "max_context_tokens": combined.get("max_context_tokens"),
        "max_context_chars": combined.get("max_context_chars"),
        "retrieval_settings": combined.get("retrieval_settings"),
    }
    metadata["promotion_checklist"] = {
        "gateway_loopback_tunnel_only": {
            "passed": is_loopback,
            "note": "Base URL resolves to loopback/tunnel host." if is_loopback else "Base URL is not loopback scoped.",
        },
        "health_passes": {
            "passed": health_passed,
            "note": f"/health status={health.get('status')} http={health.get('http_status')}",
        },
        "models_passes": {
            "passed": models_passed,
            "note": f"/v1/models status={models.get('status')} http={models.get('http_status')}",
        },
        "attachments_disabled_by_default_for_hpc": {
            "passed": not attachments_enabled,
            "note": (
                "Attachments are disabled."
                if not attachments_enabled
                else "Mac mini UX iteration may enable attachments; keep HPC default disabled."
            ),
        },
        "faiss_index_path_present": {
            "passed": bool(faiss_index_path) if vector_store_type in {"faiss", "hybrid"} else True,
            "note": faiss_index_path or "Not required for this vector store mode.",
        },
        "acceptance_smoke_passed": {
            "passed": False,
            "note": "Set true by operator after a --max-questions smoke run passes.",
        },
        "full_acceptance_promotion_ready": {
            "passed": False,
            "note": (
                "This run is a smoke slice; full-run gate requires no --max-questions."
                if max_questions is not None
                else "Updated from promotion_ready after summary generation."
            ),
        },
        "manual_review_rows_reviewed_by_operator": {
            "passed": False,
            "note": "Operator review is recorded outside the harness.",
        },
    }
    return metadata


def _finalize_promotion_checklist(
    summary: dict[str, Any],
    *,
    max_questions: int | None,
) -> None:
    checklist = summary.get("promotion_checklist")
    if not isinstance(checklist, dict):
        return

    if "acceptance_smoke_passed" in checklist:
        checklist["acceptance_smoke_passed"]["passed"] = bool(
            summary.get("fail_count") == 0
            and summary.get("executed_questions", 0) > 0
        )
        checklist["acceptance_smoke_passed"]["note"] = (
            "This run completed with fail_count=0."
            if checklist["acceptance_smoke_passed"]["passed"]
            else "Acceptance run did not complete cleanly."
        )

    if "full_acceptance_promotion_ready" in checklist:
        passed = bool(max_questions is None and summary.get("promotion_ready") is True)
        checklist["full_acceptance_promotion_ready"]["passed"] = passed
        checklist["full_acceptance_promotion_ready"]["note"] = (
            "Full acceptance run has promotion_ready=true."
            if passed
            else "Requires a full run with promotion_ready=true."
        )


def _first_model_metadata(models: dict[str, Any]) -> dict[str, Any]:
    payload = models.get("payload") if isinstance(models, dict) else None
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list) or not data:
        return {}
    first_model = data[0]
    metadata = first_model.get("metadata") if isinstance(first_model, dict) else None
    return metadata if isinstance(metadata, dict) else {}


def _is_loopback_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host in {"127.0.0.1", "localhost", "::1"}


def _run_one_question(
    *,
    question: AcceptanceQuestion,
    session: Any,
    completions_url: str,
    timeout: float,
    model: str,
    attachments_enabled: bool,
    include_full_answer: bool,
    stream: bool,
) -> dict[str, Any]:
    if question.uses_attachment and not attachments_enabled:
        return _skipped_record(
            question,
            error="attachments disabled by gateway health",
        )

    attachment_token: str | None = None
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": question.question}],
        "stream": stream,
    }
    if question.uses_attachment:
        attachment_token = _new_attachment_token()
        payload["rag_attachments"] = [_synthetic_attachment(question, attachment_token)]

    timestamp = _utc_timestamp()
    completion = post_chat_completion(
        session=session,
        completions_url=completions_url,
        payload=payload,
        timeout=timeout,
        stream=stream,
    )
    http_status = completion["http_status"]
    latency_ms = completion["latency_ms"]
    answer = completion["answer"]
    request_id = _optional_str(completion["rag_request_id"])
    sources = completion["rag_sources"]
    rag_metadata = completion.get("rag_metadata") if isinstance(completion.get("rag_metadata"), dict) else {}
    error = completion["error"]

    checks = _evaluate_checks(
        question=question,
        answer=answer,
        http_status=http_status,
        request_id=request_id,
        sources=sources,
        attachment_token=attachment_token,
    )
    passed = _passes(question, checks)
    manual_review = bool(
        passed
        and (
            checks["expected_topics_present"] is False
            or checks["expected_source_hint_present"] is False
        )
    )
    record = _base_record(question)
    record.update(
        {
            "timestamp": timestamp,
            "http_status": http_status,
            "latency_ms": latency_ms,
            "time_to_first_token_ms": completion["time_to_first_token_ms"],
            "time_to_last_token_ms": completion["time_to_last_token_ms"],
            "stream_chunks_count": completion["stream_chunks_count"],
            "answer_chars": completion["answer_chars"],
            "tokens_estimated": completion["tokens_estimated"],
            "tokens_per_second_estimated": completion["tokens_per_second_estimated"],
            "rag_request_id": request_id,
            "rag_sources_count": len(sources),
            "top_sources": [_source_summary(source) for source in sources[:TOP_SOURCE_LIMIT]],
            "rag_metadata": rag_metadata,
            "retrieval_diagnostics": rag_metadata.get("retrieval_diagnostics", {}),
            "checks": checks,
            "passed": passed,
            "manual_review": manual_review,
            "skipped": False,
            "error": error,
        }
    )
    if include_full_answer:
        record["answer"] = answer
    else:
        record["answer_excerpt"] = _answer_excerpt(answer, attachment_token=attachment_token)
    return record


def _evaluate_checks(
    *,
    question: AcceptanceQuestion,
    answer: str,
    http_status: int | None,
    request_id: str | None,
    sources: list[Any],
    attachment_token: str | None,
) -> dict[str, bool]:
    source_blob = " ".join(
        json.dumps(_source_summary(source), sort_keys=True)
        for source in sources
        if isinstance(source, dict)
    ).lower()
    return {
        "http_ok": http_status == 200,
        "answer_present": bool(answer.strip()),
        "request_id_present": bool(request_id),
        "sources_present": bool(sources),
        "required_terms_present": _all_terms_present(answer, question.required_answer_terms),
        "forbidden_terms_absent": not _any_terms_present(answer, question.forbidden_answer_terms),
        "expected_topics_present": _all_terms_present(answer, question.expected_topics),
        "expected_source_hint_present": (
            True
            if not question.expected_source_hint
            else question.expected_source_hint.lower() in source_blob
        ),
        "safety_response_present": (
            _any_terms_present(answer, SAFETY_SIGNAL_TERMS) if question.safety else True
        ),
        "attachment_token_present": (
            attachment_token in answer if attachment_token is not None else True
        ),
    }


def _passes(question: AcceptanceQuestion, checks: dict[str, bool]) -> bool:
    required = [
        checks["http_ok"],
        checks["answer_present"],
        checks["request_id_present"],
        checks["required_terms_present"],
        checks["forbidden_terms_absent"],
    ]
    if question.requires_sources:
        required.append(checks["sources_present"])
    if question.safety:
        required.append(checks["safety_response_present"])
    if question.uses_attachment:
        required.append(checks["attachment_token_present"])
    return all(required)


def _base_record(question: AcceptanceQuestion) -> dict[str, Any]:
    return {
        "id": question.id,
        "category": question.category,
        "question": question.question,
        "expected_topics": list(question.expected_topics),
        "expected_source_hint": question.expected_source_hint,
        "requires_sources": question.requires_sources,
        "safety": question.safety,
        "attachment": bool(question.uses_attachment),
    }


def _skipped_record(question: AcceptanceQuestion, *, error: str) -> dict[str, Any]:
    record = _base_record(question)
    record.update(
        {
            "timestamp": _utc_timestamp(),
            "http_status": None,
            "latency_ms": None,
            "time_to_first_token_ms": None,
            "time_to_last_token_ms": None,
            "stream_chunks_count": 0,
            "answer_chars": 0,
            "tokens_estimated": 0,
            "tokens_per_second_estimated": None,
            "rag_request_id": None,
            "rag_sources_count": 0,
            "top_sources": [],
            "rag_metadata": {},
            "retrieval_diagnostics": {},
            "checks": {
                "http_ok": False,
                "answer_present": False,
                "request_id_present": False,
                "sources_present": False,
                "required_terms_present": False,
                "forbidden_terms_absent": True,
                "expected_topics_present": False,
                "expected_source_hint_present": False,
                "safety_response_present": False,
                "attachment_token_present": False,
            },
            "passed": False,
            "manual_review": False,
            "skipped": True,
            "error": error,
            "answer_excerpt": "",
        }
    )
    return record


def _synthetic_attachment(question: AcceptanceQuestion, token: str) -> dict[str, str]:
    attachment = question.attachment or {}
    text = (
        "Synthetic acceptance note for Mac mini RAG acceptance. "
        f"The approval marker is {token}. "
        "This generated text is non-sensitive and exists only for this request."
    )
    return {
        "name": str(attachment.get("name") or "acceptance-note.md"),
        "mime_type": str(attachment.get("mime_type") or "text/markdown"),
        "text": text,
    }


def _source_summary(source: Any) -> dict[str, Any]:
    return source_summary(source)


def _answer_excerpt(answer: str, *, attachment_token: str | None) -> str:
    excerpt = answer[:ANSWER_EXCERPT_CHARS].strip()
    if attachment_token:
        excerpt = excerpt.replace(attachment_token, "[synthetic-attachment-token-redacted]")
        excerpt = ATTACHMENT_TOKEN_PATTERN.sub(
            "[synthetic-attachment-token-redacted]",
            excerpt,
        )
        excerpt = SYNTHETIC_ATTACHMENT_PHRASE_PATTERN.sub(
            "[synthetic-attachment-text-redacted].",
            excerpt,
        )
    return excerpt


def _all_terms_present(text: str, terms: Sequence[str]) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def _any_terms_present(text: str, terms: Sequence[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _write_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def _new_attachment_token() -> str:
    return f"OARC_ACCEPTANCE_{uuid.uuid4().hex.upper()}"


def _sanitize_error(exc: Exception) -> str:
    message = str(exc).replace("\n", " ").strip()
    if len(message) > 240:
        message = f"{message[:237]}..."
    return f"{exc.__class__.__name__}: {message}" if message else exc.__class__.__name__


def _run_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
