"""Tests for MLflow sanitization and metric filtering helpers."""

from __future__ import annotations

import pytest

from src.rag import mlflow_tracker


def test_sanitize_prompt_record_hashes_prompt():
    record = {
        "query_id": "q1",
        "question": "How do I submit a Slurm job?",
        "answer": "Submit via sbatch.",
        "retrieved_doc_ids": ["doc1", "doc2"],
    }
    sanitized = mlflow_tracker.sanitize_prompt_record(record, top_k=1, include_answer=True)
    assert "question" not in sanitized
    assert sanitized["retrieved_doc_ids"] == ["doc1"]
    assert len(sanitized["prompt_hash"]) == 16


def test_log_metrics_filters_non_numeric(monkeypatch: pytest.MonkeyPatch):
    captured = {}

    class DummyMlflow:
        def log_metrics(self, metrics, step=None):  # noqa: D401 - minimal stub
            captured["metrics"] = metrics
            captured["step"] = step

    monkeypatch.setattr(mlflow_tracker, "mlflow", DummyMlflow())
    monkeypatch.setattr(mlflow_tracker, "_mlflow_enabled", lambda: True)

    mlflow_tracker.log_metrics(
        {"latency_ms": 12.5, "retrieval_count": 4, "ignore": "not-a-number"},
        step=3,
    )

    assert captured["metrics"] == {"latency_ms": 12.5, "retrieval_count": 4.0}
    assert captured["step"] == 3
