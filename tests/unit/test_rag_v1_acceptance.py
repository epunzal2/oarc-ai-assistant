"""Tests for the Mac mini RAG v1 acceptance harness."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from src.evaluation.acceptance import (
    DEFAULT_COMPLETIONS_URL,
    _all_terms_present,
    _any_terms_present,
    build_health_url,
    load_questions,
    normalize_completions_url,
    parse_args,
    run_acceptance,
    summarize_results,
)

ROOT = Path(__file__).resolve().parents[2]


class FakeResponse:
    """Small response fake for acceptance harness HTTP calls."""

    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self) -> dict:
        return self._payload


class FakeSession:
    """Session fake that records requests and returns deterministic responses."""

    def __init__(self, *, attachments_enabled: bool = True) -> None:
        self.attachments_enabled = attachments_enabled
        self.posts: list[dict] = []
        self.synthetic_tokens: list[str] = []

    def get(self, url: str, *, timeout: float) -> FakeResponse:
        return FakeResponse(
            200,
            {
                "status": "ok",
                "ui": {"attachments_enabled": self.attachments_enabled},
            },
        )

    def post(self, url: str, *, json: dict, timeout: float, stream: bool = False) -> FakeResponse:
        self.posts.append(json)
        sources = [
            {
                "title": "Slurm Quickstart",
                "chunk_id": "slurm-submit-1",
                "source": "docs/slurm/quickstart.md",
                "url": "https://example.edu/slurm",
            }
        ]
        if json.get("rag_attachments"):
            text = json["rag_attachments"][0]["text"]
            token = re.search(r"OARC_ACCEPTANCE_[A-Z0-9_]+", text).group(0)
            self.synthetic_tokens.append(token)
            answer = f"The synthetic marker is {token}."
        else:
            answer = "Use sbatch to submit a Slurm batch script."
        return FakeResponse(
            200,
            {
                "rag_request_id": "rag-test",
                "rag_sources": sources,
                "choices": [{"message": {"content": answer}}],
            },
        )


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_load_questions_validates_required_fields_duplicates_and_max(tmp_path: Path) -> None:
    questions_path = tmp_path / "questions.jsonl"
    _write_jsonl(
        questions_path,
        [
            {
                "id": "q1",
                "category": "slurm_basics",
                "question": "How do I submit a job?",
            },
            {
                "id": "q2",
                "category": "amarel_access",
                "question": "How do I log in?",
            },
        ],
    )

    assert [question.id for question in load_questions(questions_path, max_questions=1)] == ["q1"]
    assert [
        question.id
        for question in load_questions(questions_path, question_ids=["q2", "q1", "q2"])
    ] == ["q1", "q2"]
    assert [
        question.id
        for question in load_questions(
            questions_path,
            max_questions=1,
            question_ids=["q2", "q1"],
        )
    ] == ["q1"]
    with pytest.raises(ValueError, match="question id\\(s\\) not found: missing"):
        load_questions(questions_path, question_ids=["missing"])

    _write_jsonl(
        questions_path,
        [
            {
                "id": "duplicate",
                "category": "slurm_basics",
                "question": "How do I submit a job?",
            },
            {
                "id": "duplicate",
                "category": "slurm_basics",
                "question": "How do I cancel a job?",
            },
        ],
    )
    with pytest.raises(ValueError, match="duplicate question id"):
        load_questions(questions_path)

    _write_jsonl(questions_path, [{"id": "missing", "category": "slurm_basics"}])
    with pytest.raises(ValueError, match="missing required field"):
        load_questions(questions_path)


def test_cli_defaults_and_url_normalization() -> None:
    args = parse_args([])

    assert args.base_url == DEFAULT_COMPLETIONS_URL
    assert args.stream is True
    assert args.question_id == []
    assert args.max_p95_latency_ms == 15000.0
    assert args.max_p95_ttft_ms == 10000.0
    targeted_args = parse_args(["--question-id", "q2", "--include-full-answer"])
    assert targeted_args.question_id == ["q2"]
    assert targeted_args.include_full_answer is True
    assert normalize_completions_url("http://127.0.0.1:18088") == (
        "http://127.0.0.1:18088/v1/chat/completions"
    )
    assert normalize_completions_url("http://127.0.0.1:18088/v1") == (
        "http://127.0.0.1:18088/v1/chat/completions"
    )
    assert normalize_completions_url("http://127.0.0.1:18088/v1/chat/completions") == (
        "http://127.0.0.1:18088/v1/chat/completions"
    )
    assert build_health_url("http://127.0.0.1:18088/v1/chat/completions") == (
        "http://127.0.0.1:18088/health"
    )


def test_cli_wrapper_runs_from_repo_root() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/evaluation/run_v1_acceptance.py", "--help"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--base-url" in result.stdout


def test_expected_topic_matching_normalizes_cli_placeholders() -> None:
    assert _all_terms_present("Run scancel <job_id>.", ["scancel", "job id"])
    assert _all_terms_present("Use job-id with scancel.", ["job_id"])


def test_safety_forbidden_terms_do_not_match_short_secret_prefixes() -> None:
    refusal = "I cannot reveal secrets. The information you are asking for is not available."

    assert not _any_terms_present(refusal, ["sk-proj", "sk_live", "api_key="])


def test_summarize_results_reports_latency_failures_and_review_lists() -> None:
    summary = summarize_results(
        [
            {
                "id": "q1",
                "category": "slurm_basics",
                "skipped": False,
                "passed": True,
                "manual_review": False,
                "latency_ms": 100,
                "rag_sources_count": 2,
            },
            {
                "id": "q2",
                "category": "slurm_basics",
                "skipped": False,
                "passed": False,
                "manual_review": False,
                "latency_ms": 200,
                "rag_sources_count": 0,
            },
            {
                "id": "q3",
                "category": "amarel_access",
                "skipped": False,
                "passed": True,
                "manual_review": True,
                "latency_ms": 300,
                "rag_sources_count": 1,
            },
            {
                "id": "q4",
                "category": "attachment_optional",
                "skipped": True,
                "passed": False,
                "manual_review": False,
            },
        ],
        attachments_enabled=False,
    )

    assert summary["total_questions"] == 4
    assert summary["executed_questions"] == 3
    assert summary["skipped_questions"] == 1
    assert summary["pass_count"] == 2
    assert summary["fail_count"] == 1
    assert summary["p50_latency_ms"] == 200
    assert summary["p95_latency_ms"] == 300
    assert summary["failures_by_category"] == {"slurm_basics": 1}
    assert summary["zero_source_question_ids"] == ["q2"]
    assert summary["manual_review_question_ids"] == ["q3"]
    assert summary["attachments_enabled"] is False


def test_run_acceptance_writes_excerpt_only_results_and_redacts_attachment_token(
    tmp_path: Path,
) -> None:
    questions_path = tmp_path / "questions.jsonl"
    _write_jsonl(
        questions_path,
        [
            {
                "id": "slurm_submit",
                "category": "slurm_basics",
                "question": "How do I submit a job?",
                "required_answer_terms": ["sbatch"],
            },
            {
                "id": "attachment_marker",
                "category": "attachment_optional",
                "question": "What is the synthetic marker in the attached note?",
                "attachment": {
                    "enabled": True,
                    "name": "acceptance-note.md",
                    "mime_type": "text/markdown",
                },
                "requires_sources": False,
            },
        ],
    )
    session = FakeSession(attachments_enabled=True)

    result = run_acceptance(
        base_url="http://127.0.0.1:18088",
        questions_path=questions_path,
        output_dir=tmp_path / "outputs",
        timeout=1.0,
        model="oarc-rag-v1",
        include_full_answer=False,
        stream=False,
        session=session,
        run_timestamp="20260528T120000Z",
    )

    results_text = result.results_path.read_text(encoding="utf-8")
    records = [json.loads(line) for line in results_text.splitlines()]
    attachment_record = records[1]
    token = session.synthetic_tokens[0]

    assert result.summary["total_questions"] == 2
    assert result.summary["fail_count"] == 0
    assert len(session.posts) == 2
    assert "answer" not in records[0]
    assert "answer_excerpt" in records[0]
    assert attachment_record["checks"]["attachment_token_present"] is True
    assert token not in results_text
    assert "Synthetic acceptance note" not in results_text
    assert "[synthetic-attachment-token-redacted]" in attachment_record["answer_excerpt"]


def test_run_acceptance_can_deliberately_capture_full_answers(tmp_path: Path) -> None:
    questions_path = tmp_path / "questions.jsonl"
    _write_jsonl(
        questions_path,
        [
            {
                "id": "attachment_marker",
                "category": "attachment_optional",
                "question": "What is the synthetic marker in the attached note?",
                "attachment": {
                    "enabled": True,
                    "name": "acceptance-note.md",
                    "mime_type": "text/markdown",
                },
                "requires_sources": False,
            },
        ],
    )
    session = FakeSession(attachments_enabled=True)

    result = run_acceptance(
        base_url="http://127.0.0.1:18088",
        questions_path=questions_path,
        output_dir=tmp_path / "outputs",
        timeout=1.0,
        model="oarc-rag-v1",
        include_full_answer=True,
        stream=False,
        session=session,
        run_timestamp="20260528T120000Z",
    )

    results_text = result.results_path.read_text(encoding="utf-8")

    assert session.synthetic_tokens[0] in results_text
    assert '"answer"' in results_text


def test_attachment_question_is_skipped_when_gateway_disables_attachments(
    tmp_path: Path,
) -> None:
    questions_path = tmp_path / "questions.jsonl"
    _write_jsonl(
        questions_path,
        [
            {
                "id": "attachment_marker",
                "category": "attachment_optional",
                "question": "What is the synthetic marker in the attached note?",
                "attachment": {
                    "enabled": True,
                    "name": "acceptance-note.md",
                    "mime_type": "text/markdown",
                },
            },
        ],
    )
    session = FakeSession(attachments_enabled=False)

    result = run_acceptance(
        base_url="http://127.0.0.1:18088",
        questions_path=questions_path,
        output_dir=tmp_path / "outputs",
        timeout=1.0,
        model="oarc-rag-v1",
        include_full_answer=False,
        stream=False,
        session=session,
        run_timestamp="20260528T120000Z",
    )

    records = [
        json.loads(line)
        for line in result.results_path.read_text(encoding="utf-8").splitlines()
    ]
    assert result.summary["skipped_questions"] == 1
    assert records[0]["skipped"] is True
    assert records[0]["error"] == "attachments disabled by gateway health"
    assert records[0]["time_to_first_token_ms"] is None
    assert records[0]["stream_chunks_count"] == 0
    assert records[0]["tokens_estimated"] == 0
    assert session.posts == []
