"""Tests for acceptance Markdown reports and run comparisons."""

from __future__ import annotations

import json
from pathlib import Path

from src.evaluation.acceptance_report import (
    compare_acceptance_runs,
    render_acceptance_report,
    write_acceptance_report,
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _summary(**overrides) -> dict:
    summary = {
        "run_dir": "logs/rag_v1_acceptance/test",
        "results_path": "logs/rag_v1_acceptance/test/results.jsonl",
        "summary_path": "logs/rag_v1_acceptance/test/summary.json",
        "base_url": "http://127.0.0.1:18088/v1/chat/completions",
        "model": "oarc-rag-v1",
        "backend_model": "llama3.2:1b",
        "vector_store_type": "faiss",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "faiss_index_path": "vector_index/faiss_macmini",
        "retrieval_mode": "vector",
        "attachments_enabled": False,
        "total_questions": 1,
        "executed_questions": 1,
        "skipped_questions": 0,
        "pass_count": 1,
        "fail_count": 0,
        "p50_latency_ms": 100.0,
        "p95_latency_ms": 100.0,
        "p50_time_to_first_token_ms": 20.0,
        "p95_time_to_first_token_ms": 20.0,
        "p50_positive_rag_sources_count": 2.0,
        "p95_positive_rag_sources_count": 2.0,
        "zero_source_question_ids": [],
        "manual_review_question_ids": ["q1"],
        "promotion_ready": True,
        "automated_gates": {
            "full_acceptance_passed": {"passed": True, "fail_count": 0},
            "p95_latency_below_threshold": {
                "passed": True,
                "value_ms": 100.0,
                "threshold_ms": 15000.0,
            },
        },
        "promotion_checklist": {
            "gateway_loopback_tunnel_only": {
                "passed": True,
                "note": "Base URL is loopback scoped.",
            },
            "manual_review_rows_reviewed_by_operator": {
                "passed": False,
                "note": "Operator review is recorded outside the harness.",
            },
        },
        "full_answers_included": False,
    }
    summary.update(overrides)
    return summary


def _records() -> list[dict]:
    return [
        {
            "id": "q1",
            "category": "slurm_basics",
            "question": "How do I submit a job?",
            "passed": True,
            "manual_review": True,
            "rag_sources_count": 2,
            "latency_ms": 100.0,
            "time_to_first_token_ms": 20.0,
            "top_sources": [
                {
                    "title": "Slurm Quickstart",
                    "source": "docs/slurm/quickstart.md",
                    "chunk_id": "chunk-1",
                }
            ],
            "answer_excerpt": "Use sbatch.",
            "answer": "FULL ANSWER SHOULD NOT RENDER",
        }
    ]


def test_render_acceptance_report_is_excerpt_only_by_default() -> None:
    report = render_acceptance_report(_summary(), _records())

    assert "# RAG v1 Acceptance Report" in report
    assert "llama3.2:1b" in report
    assert "RAG_RETRIEVAL_MODE" in report
    assert "Slurm Quickstart" in report
    assert "Use sbatch." in report
    assert "FULL ANSWER SHOULD NOT RENDER" not in report
    assert "manual_review_rows_reviewed_by_operator" in report


def test_write_acceptance_report_persists_report_path(tmp_path: Path) -> None:
    summary = _summary(run_dir=str(tmp_path))
    report_path = write_acceptance_report(tmp_path, summary, _records())

    assert report_path == tmp_path / "report.md"
    assert report_path.exists()
    assert summary["report_path"] == str(report_path)
    assert summary["plot_paths"]["latency_by_question"] == str(
        tmp_path / "plots" / "latency-by-question.svg"
    )
    assert summary["plot_paths"]["ttft_by_question"] == str(
        tmp_path / "plots" / "ttft-by-question.svg"
    )
    assert summary["plot_paths"]["source_counts_by_question"] == str(
        tmp_path / "plots" / "source-counts-by-question.svg"
    )
    assert (tmp_path / "plots" / "latency-by-question.svg").exists()
    assert "## Plots" in report_path.read_text(encoding="utf-8")
    assert "plots/latency-by-question.svg" in report_path.read_text(encoding="utf-8")


def test_compare_acceptance_runs_writes_comparison_to_newer_run(tmp_path: Path) -> None:
    run_a = tmp_path / "20260529T000000Z"
    run_b = tmp_path / "20260529T010000Z"
    run_a.mkdir()
    run_b.mkdir()

    (run_a / "summary.json").write_text(
        json.dumps(
            _summary(
                run_dir=str(run_a),
                backend_model="llama3.2:1b",
                p95_latency_ms=5000.0,
                p95_time_to_first_token_ms=1000.0,
                manual_review_question_ids=["q1"],
            )
        ),
        encoding="utf-8",
    )
    _write_jsonl(run_a / "results.jsonl", _records())
    (run_b / "summary.json").write_text(
        json.dumps(
            _summary(
                run_dir=str(run_b),
                backend_model="llama3.2:3b",
                p95_latency_ms=9000.0,
                p95_time_to_first_token_ms=2500.0,
                manual_review_question_ids=["q1", "q2"],
            )
        ),
        encoding="utf-8",
    )
    _write_jsonl(run_b / "results.jsonl", _records())

    comparison = compare_acceptance_runs(run_a, run_b, write_report=True)

    assert comparison["run_a"]["backend_model"] == "llama3.2:1b"
    assert comparison["run_b"]["backend_model"] == "llama3.2:3b"
    assert comparison["deltas"]["p95_latency_ms"] == 4000.0
    assert comparison["deltas"]["manual_review_count"] == 1
    assert (run_b / "comparison.md").exists()
