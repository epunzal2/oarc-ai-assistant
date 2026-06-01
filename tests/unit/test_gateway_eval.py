"""Tests for reusable gateway evaluation helpers."""

from __future__ import annotations

import json

from src.evaluation.gateway_eval import (
    DEFAULT_MAX_P95_LATENCY_MS,
    DEFAULT_MAX_P95_TTFT_MS,
    GatewayEvalThresholds,
    build_models_url,
    post_chat_completion,
    summarize_gateway_results,
)


class StreamingResponse:
    """Small streaming response fake for OpenAI-style SSE parsing."""

    status_code = 200
    text = ""

    def __init__(self, events: list[dict]) -> None:
        self.events = events

    def iter_lines(self, decode_unicode: bool = False):
        for event in self.events:
            yield f"data: {json.dumps(event)}"
        yield "data: [DONE]"

    def json(self) -> dict:
        return {}


class StreamingSession:
    """Session fake that returns a deterministic streamed chat response."""

    def __init__(self) -> None:
        self.posts: list[dict] = []

    def post(self, url: str, *, json: dict, timeout: float, stream: bool = False):
        self.posts.append({"url": url, "json": json, "timeout": timeout, "stream": stream})
        return StreamingResponse(
            [
                {"choices": [{"delta": {"role": "assistant"}, "finish_reason": None}]},
                {"choices": [{"delta": {"content": "Use "}, "finish_reason": None}]},
                {"choices": [{"delta": {"content": "sbatch."}, "finish_reason": None}]},
                {
                    "choices": [{"delta": {}, "finish_reason": "stop"}],
                    "rag_request_id": "rag-stream",
                    "rag_sources": [
                        {
                            "title": "Slurm",
                            "chunk_id": "chunk-1",
                            "source": "slurm.md",
                        }
                    ],
                    "rag_metadata": {
                        "retrieval_diagnostics": {
                            "retrieval_mode": "vector",
                            "final_count": 1,
                        }
                    },
                },
            ]
        )


def test_post_chat_completion_streaming_records_ttft_and_sources() -> None:
    session = StreamingSession()

    result = post_chat_completion(
        session=session,
        completions_url="http://127.0.0.1:18088/v1/chat/completions",
        payload={"model": "oarc-rag-v1", "messages": [], "stream": True},
        timeout=1.0,
        stream=True,
    )

    assert session.posts[0]["stream"] is True
    assert result["http_status"] == 200
    assert result["answer"] == "Use sbatch."
    assert result["rag_request_id"] == "rag-stream"
    assert result["rag_sources_count"] == 1
    assert result["rag_metadata"]["retrieval_diagnostics"]["final_count"] == 1
    assert result["stream_chunks_count"] == 2
    assert result["time_to_first_token_ms"] is not None
    assert result["time_to_last_token_ms"] is not None
    assert result["answer_chars"] == len("Use sbatch.")
    assert result["tokens_estimated"] == 2
    assert result["tokens_per_second_estimated"] is not None


def test_build_models_url_accepts_gateway_root_v1_and_completions_urls() -> None:
    assert build_models_url("http://127.0.0.1:18088") == "http://127.0.0.1:18088/v1/models"
    assert build_models_url("http://127.0.0.1:18088/v1") == (
        "http://127.0.0.1:18088/v1/models"
    )
    assert build_models_url("http://127.0.0.1:18088/v1/chat/completions") == (
        "http://127.0.0.1:18088/v1/models"
    )


def test_summarize_gateway_results_adds_automated_gates() -> None:
    summary = summarize_gateway_results(
        [
            {
                "id": "q1",
                "category": "slurm_basics",
                "skipped": False,
                "passed": True,
                "manual_review": False,
                "latency_ms": 1000.0,
                "time_to_first_token_ms": 100.0,
                "rag_sources_count": 1,
                "requires_sources": True,
            },
            {
                "id": "q2",
                "category": "negative_safety",
                "skipped": False,
                "passed": True,
                "manual_review": False,
                "latency_ms": 2000.0,
                "time_to_first_token_ms": 200.0,
                "rag_sources_count": 0,
                "requires_sources": False,
            },
        ],
        attachments_enabled=True,
        thresholds=GatewayEvalThresholds(
            max_p95_latency_ms=2500.0,
            max_p95_ttft_ms=250.0,
        ),
    )

    gates = summary["automated_gates"]

    assert summary["p95_latency_ms"] == 2000.0
    assert summary["p95_time_to_first_token_ms"] == 200.0
    assert summary["p50_rag_sources_count"] == 0.0
    assert summary["p95_rag_sources_count"] == 1.0
    assert summary["p50_positive_rag_sources_count"] == 1.0
    assert summary["p95_positive_rag_sources_count"] == 1.0
    assert gates["full_acceptance_passed"]["passed"] is True
    assert gates["p95_latency_below_threshold"]["passed"] is True
    assert gates["p95_ttft_below_threshold"]["passed"] is True
    assert gates["positive_rag_sources_present"]["passed"] is True
    assert summary["promotion_ready"] is True
    assert summary["thresholds"] == {
        "max_p95_latency_ms": 2500.0,
        "max_p95_ttft_ms": 250.0,
    }


def test_summarize_gateway_results_fails_positive_zero_source_gate() -> None:
    summary = summarize_gateway_results(
        [
            {
                "id": "q1",
                "category": "slurm_basics",
                "skipped": False,
                "passed": True,
                "manual_review": False,
                "latency_ms": 100.0,
                "time_to_first_token_ms": 10.0,
                "rag_sources_count": 0,
                "requires_sources": True,
            }
        ],
        attachments_enabled=True,
        thresholds=GatewayEvalThresholds(),
    )

    assert summary["automated_gates"]["positive_rag_sources_present"]["passed"] is False
    assert summary["zero_source_positive_question_ids"] == ["q1"]
    assert summary["promotion_ready"] is False
    assert summary["thresholds"]["max_p95_latency_ms"] == DEFAULT_MAX_P95_LATENCY_MS
    assert summary["thresholds"]["max_p95_ttft_ms"] == DEFAULT_MAX_P95_TTFT_MS
