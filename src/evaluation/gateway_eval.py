"""Reusable gateway evaluation helpers for RAG acceptance and future evals."""

from __future__ import annotations

import json
import math
import time
from collections import Counter
from dataclasses import dataclass
from typing import Any, Sequence

DEFAULT_MAX_P95_LATENCY_MS = 15_000.0
DEFAULT_MAX_P95_TTFT_MS = 10_000.0


@dataclass(frozen=True)
class GatewayEvalThresholds:
    """Automated promotion-gate thresholds for gateway evaluations."""

    max_p95_latency_ms: float = DEFAULT_MAX_P95_LATENCY_MS
    max_p95_ttft_ms: float = DEFAULT_MAX_P95_TTFT_MS

    def as_dict(self) -> dict[str, float]:
        return {
            "max_p95_latency_ms": self.max_p95_latency_ms,
            "max_p95_ttft_ms": self.max_p95_ttft_ms,
        }


def normalize_completions_url(base_url: str) -> str:
    """Return a full `/v1/chat/completions` URL from accepted gateway URL forms."""

    normalized = base_url.rstrip("/")
    if normalized.endswith("/v1/chat/completions"):
        return normalized
    if normalized.endswith("/v1"):
        return f"{normalized}/chat/completions"
    return f"{normalized}/v1/chat/completions"


def build_health_url(completions_url: str) -> str:
    """Return the sibling gateway `/health` URL for a completions endpoint."""

    suffix = "/v1/chat/completions"
    normalized = completions_url.rstrip("/")
    if normalized.endswith(suffix):
        return f"{normalized[: -len(suffix)]}/health"
    return f"{normalized}/health"


def build_models_url(completions_url: str) -> str:
    """Return the sibling gateway `/v1/models` URL for a completions endpoint."""

    suffix = "/v1/chat/completions"
    normalized = completions_url.rstrip("/")
    if normalized.endswith(suffix):
        return f"{normalized[: -len('/chat/completions')]}/models"
    if normalized.endswith("/v1"):
        return f"{normalized}/models"
    return f"{normalized}/v1/models"


def post_chat_completion(
    *,
    session: Any,
    completions_url: str,
    payload: dict[str, Any],
    timeout: float,
    stream: bool,
) -> dict[str, Any]:
    """Post one chat request and return normalized response plus timing metrics."""

    started_at = time.perf_counter()
    try:
        if stream:
            return _post_streaming_completion(
                session=session,
                completions_url=completions_url,
                payload={**payload, "stream": True},
                timeout=timeout,
                started_at=started_at,
            )
        return _post_non_streaming_completion(
            session=session,
            completions_url=completions_url,
            payload={**payload, "stream": False},
            timeout=timeout,
            started_at=started_at,
        )
    except Exception as exc:
        latency_ms = _elapsed_ms(started_at)
        return {
            "http_status": None,
            "latency_ms": latency_ms,
            "time_to_first_token_ms": None,
            "time_to_last_token_ms": None,
            "stream_chunks_count": 0,
            "answer": "",
            "answer_chars": 0,
            "tokens_estimated": 0,
            "tokens_per_second_estimated": None,
            "rag_request_id": None,
            "rag_sources": [],
            "rag_sources_count": 0,
            "rag_metadata": {},
            "error": _sanitize_error(exc),
        }


def summarize_gateway_results(
    records: Sequence[dict[str, Any]],
    *,
    attachments_enabled: bool,
    thresholds: GatewayEvalThresholds,
) -> dict[str, Any]:
    """Aggregate gateway evaluation records and automated promotion gates."""

    executed = [record for record in records if not record.get("skipped")]
    skipped = [record for record in records if record.get("skipped")]
    failed = [record for record in executed if not record.get("passed")]
    passed = [record for record in executed if record.get("passed")]
    latencies = _numeric_values(executed, "latency_ms")
    ttfts = _numeric_values(executed, "time_to_first_token_ms")
    last_tokens = _numeric_values(executed, "time_to_last_token_ms")
    source_counts = _numeric_values(executed, "rag_sources_count")
    positive_source_counts = _numeric_values(
        [record for record in executed if record.get("requires_sources")],
        "rag_sources_count",
    )
    failures_by_category = Counter(str(record.get("category")) for record in failed)
    zero_source_positive_ids = [
        str(record.get("id"))
        for record in executed
        if record.get("requires_sources") and int(record.get("rag_sources_count") or 0) == 0
    ]

    p95_latency = percentile_nearest_rank(latencies, 95)
    p95_ttft = percentile_nearest_rank(ttfts, 95)
    automated_gates = {
        "full_acceptance_passed": {
            "passed": len(failed) == 0,
            "fail_count": len(failed),
        },
        "p95_latency_below_threshold": {
            "passed": p95_latency is not None and p95_latency <= thresholds.max_p95_latency_ms,
            "value_ms": p95_latency,
            "threshold_ms": thresholds.max_p95_latency_ms,
        },
        "p95_ttft_below_threshold": {
            "passed": p95_ttft is not None and p95_ttft <= thresholds.max_p95_ttft_ms,
            "value_ms": p95_ttft,
            "threshold_ms": thresholds.max_p95_ttft_ms,
        },
        "positive_rag_sources_present": {
            "passed": not zero_source_positive_ids,
            "zero_source_positive_question_ids": zero_source_positive_ids,
        },
    }

    return {
        "total_questions": len(records),
        "executed_questions": len(executed),
        "skipped_questions": len(skipped),
        "pass_count": len(passed),
        "fail_count": len(failed),
        "p50_latency_ms": percentile_nearest_rank(latencies, 50),
        "p95_latency_ms": p95_latency,
        "p50_time_to_first_token_ms": percentile_nearest_rank(ttfts, 50),
        "p95_time_to_first_token_ms": p95_ttft,
        "p50_time_to_last_token_ms": percentile_nearest_rank(last_tokens, 50),
        "p95_time_to_last_token_ms": percentile_nearest_rank(last_tokens, 95),
        "p50_rag_sources_count": percentile_nearest_rank(source_counts, 50),
        "p95_rag_sources_count": percentile_nearest_rank(source_counts, 95),
        "min_rag_sources_count": min(source_counts) if source_counts else None,
        "max_rag_sources_count": max(source_counts) if source_counts else None,
        "p50_positive_rag_sources_count": percentile_nearest_rank(positive_source_counts, 50),
        "p95_positive_rag_sources_count": percentile_nearest_rank(positive_source_counts, 95),
        "min_positive_rag_sources_count": (
            min(positive_source_counts) if positive_source_counts else None
        ),
        "max_positive_rag_sources_count": (
            max(positive_source_counts) if positive_source_counts else None
        ),
        "failures_by_category": dict(sorted(failures_by_category.items())),
        "zero_source_question_ids": [
            str(record.get("id"))
            for record in executed
            if int(record.get("rag_sources_count") or 0) == 0
        ],
        "zero_source_positive_question_ids": zero_source_positive_ids,
        "manual_review_question_ids": [
            str(record.get("id")) for record in executed if record.get("manual_review")
        ],
        "skipped_question_ids": [str(record.get("id")) for record in skipped],
        "attachments_enabled": attachments_enabled,
        "thresholds": thresholds.as_dict(),
        "automated_gates": automated_gates,
        "promotion_ready": all(gate["passed"] for gate in automated_gates.values()),
    }


def source_summary(source: Any) -> dict[str, Any]:
    """Return source fields that are safe and useful for evaluation artifacts."""

    if not isinstance(source, dict):
        return {}
    keep = (
        "title",
        "source_title",
        "chunk_id",
        "source",
        "source_path",
        "path",
        "url",
        "id",
        "source_id",
        "score",
    )
    return {key: source[key] for key in keep if key in source and source[key] not in (None, "")}


def percentile_nearest_rank(values: Sequence[float], percentile: int) -> float | None:
    """Compute nearest-rank percentile for a small evaluation sample."""

    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil((percentile / 100.0) * len(ordered)) - 1))
    return ordered[index]


def _post_streaming_completion(
    *,
    session: Any,
    completions_url: str,
    payload: dict[str, Any],
    timeout: float,
    started_at: float,
) -> dict[str, Any]:
    response = session.post(completions_url, json=payload, timeout=timeout, stream=True)
    answer_parts: list[str] = []
    rag_request_id: str | None = None
    rag_sources: list[Any] = []
    rag_metadata: dict[str, Any] = {}
    first_token_ms: float | None = None
    last_token_ms: float | None = None
    stream_chunks_count = 0

    for raw_line in response.iter_lines(decode_unicode=True):
        line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else str(raw_line)
        if not line.startswith("data: "):
            continue
        data = line.removeprefix("data: ").strip()
        if data == "[DONE]":
            break
        try:
            event = json.loads(data)
        except json.JSONDecodeError:
            continue

        if event.get("rag_request_id"):
            rag_request_id = str(event["rag_request_id"])
        if isinstance(event.get("rag_sources"), list):
            rag_sources = event["rag_sources"]
        if isinstance(event.get("rag_metadata"), dict):
            rag_metadata = event["rag_metadata"]

        content = _delta_content(event)
        if not content:
            continue
        if first_token_ms is None:
            first_token_ms = _elapsed_ms(started_at)
        last_token_ms = _elapsed_ms(started_at)
        stream_chunks_count += 1
        answer_parts.append(content)

    latency_ms = _elapsed_ms(started_at)
    answer = "".join(answer_parts)
    return _completion_record(
        http_status=int(response.status_code),
        latency_ms=latency_ms,
        time_to_first_token_ms=first_token_ms,
        time_to_last_token_ms=last_token_ms,
        stream_chunks_count=stream_chunks_count,
        answer=answer,
        rag_request_id=rag_request_id,
        rag_sources=rag_sources,
        rag_metadata=rag_metadata,
        error=None,
    )


def _post_non_streaming_completion(
    *,
    session: Any,
    completions_url: str,
    payload: dict[str, Any],
    timeout: float,
    started_at: float,
) -> dict[str, Any]:
    response = session.post(completions_url, json=payload, timeout=timeout)
    latency_ms = _elapsed_ms(started_at)
    try:
        response_payload = response.json()
    except Exception:
        response_payload = {}
    rag_sources = response_payload.get("rag_sources") if isinstance(response_payload, dict) else []
    if not isinstance(rag_sources, list):
        rag_sources = []
    request_id = response_payload.get("rag_request_id") if isinstance(response_payload, dict) else None
    rag_metadata = (
        response_payload.get("rag_metadata")
        if isinstance(response_payload, dict)
        and isinstance(response_payload.get("rag_metadata"), dict)
        else {}
    )
    return _completion_record(
        http_status=int(response.status_code),
        latency_ms=latency_ms,
        time_to_first_token_ms=None,
        time_to_last_token_ms=None,
        stream_chunks_count=0,
        answer=_extract_answer(response_payload),
        rag_request_id=str(request_id) if request_id else None,
        rag_sources=rag_sources,
        rag_metadata=rag_metadata,
        error=None,
    )


def _completion_record(
    *,
    http_status: int | None,
    latency_ms: float | None,
    time_to_first_token_ms: float | None,
    time_to_last_token_ms: float | None,
    stream_chunks_count: int,
    answer: str,
    rag_request_id: str | None,
    rag_sources: list[Any],
    rag_metadata: dict[str, Any] | None,
    error: str | None,
) -> dict[str, Any]:
    tokens_estimated = _estimate_tokens(answer)
    return {
        "http_status": http_status,
        "latency_ms": latency_ms,
        "time_to_first_token_ms": time_to_first_token_ms,
        "time_to_last_token_ms": time_to_last_token_ms,
        "stream_chunks_count": stream_chunks_count,
        "answer": answer,
        "answer_chars": len(answer),
        "tokens_estimated": tokens_estimated,
        "tokens_per_second_estimated": _tokens_per_second(
            tokens_estimated,
            latency_ms,
            time_to_first_token_ms,
        ),
        "rag_request_id": rag_request_id,
        "rag_sources": rag_sources,
        "rag_sources_count": len(rag_sources),
        "rag_metadata": rag_metadata or {},
        "error": error,
    }


def _delta_content(event: dict[str, Any]) -> str:
    try:
        choices = event.get("choices") or []
        delta = choices[0].get("delta") or {}
        content = delta.get("content")
        return content if isinstance(content, str) else ""
    except (AttributeError, IndexError, KeyError, TypeError):
        return ""


def _extract_answer(payload: dict[str, Any]) -> str:
    try:
        choices = payload.get("choices") or []
        message = choices[0].get("message") or {}
        content = message.get("content")
        return content if isinstance(content, str) else ""
    except (AttributeError, IndexError, KeyError, TypeError):
        return ""


def _numeric_values(records: Sequence[dict[str, Any]], field: str) -> list[float]:
    return [
        float(record[field])
        for record in records
        if isinstance(record.get(field), (int, float))
    ]


def _estimate_tokens(text: str) -> int:
    return len(str(text or "").split())


def _tokens_per_second(
    tokens_estimated: int,
    latency_ms: float | None,
    time_to_first_token_ms: float | None,
) -> float | None:
    if not tokens_estimated or not isinstance(latency_ms, (int, float)) or latency_ms <= 0:
        return None
    generation_ms = latency_ms
    if isinstance(time_to_first_token_ms, (int, float)) and latency_ms > time_to_first_token_ms:
        generation_ms = latency_ms - time_to_first_token_ms
    if generation_ms <= 0:
        return None
    return round(tokens_estimated / (generation_ms / 1000.0), 2)


def _elapsed_ms(started_at: float) -> float:
    return round((time.perf_counter() - started_at) * 1000.0, 2)


def _sanitize_error(exc: Exception) -> str:
    message = str(exc).replace("\n", " ").strip()
    if len(message) > 240:
        message = f"{message[:237]}..."
    return f"{exc.__class__.__name__}: {message}" if message else exc.__class__.__name__
