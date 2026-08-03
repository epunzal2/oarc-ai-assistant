"""Tests for deterministic acceptance-question drafting."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.evaluation import question_drafting as drafting

ROOT = Path(__file__).resolve().parents[2]


def test_draft_acceptance_questions_from_markdown_and_dedupe(tmp_path: Path) -> None:
    source_dir = tmp_path / "docs" / "public"
    source_dir.mkdir(parents=True)
    (source_dir / "slurm.md").write_text(
        """# Slurm Jobs

## Submit jobs

Use sbatch with a batch script to submit work to Slurm. The script should describe resources,
runtime, output handling, and any modules needed before the program runs on Amarel. Keep the
commands reproducible and check the generated stdout and stderr files after submission.

## Check jobs

Use squeue to check queued or running Slurm jobs. It can show job identifiers, states, partitions,
nodes, and names for work submitted under your account. This helps users decide whether a job is
pending, running, or no longer present in the queue before they contact support.
""",
        encoding="utf-8",
    )
    existing = tmp_path / "existing.jsonl"
    existing.write_text(
        json.dumps(
            {
                "id": "slurm_basics_submit_jobs_sbatch",
                "category": "slurm_basics",
                "question": "What should I include when submitting a Slurm batch job with sbatch?",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    records = drafting.draft_acceptance_questions(
        repo_root=tmp_path,
        source_paths=[Path("docs/public")],
        existing_questions_path=existing,
        max_questions=3,
    )

    assert len(records) == 1
    assert records[0]["question"] == "How do I check queued or running Slurm jobs with squeue?"
    assert records[0]["category"] == "slurm_basics"
    assert records[0]["expected_source_hint"] == "slurm"
    assert "squeue" in records[0]["required_answer_terms"]
    assert records[0]["source_path"] == "docs/public/slurm.md"
    assert "reference_answer_excerpt" in records[0]


def test_drafter_blocks_servicenow_source_roots(tmp_path: Path) -> None:
    (tmp_path / "docs" / "servicenow").mkdir(parents=True)

    with pytest.raises(ValueError, match="source path is blocked"):
        drafting.iter_markdown_files(tmp_path, [Path("docs/servicenow")])


def test_write_jsonl_and_wrapper_help(tmp_path: Path) -> None:
    output = tmp_path / "candidates.jsonl"
    records = [
        {
            "id": "q1",
            "category": "slurm_basics",
            "question": "How do I submit?",
            "expected_topics": ["sbatch"],
        }
    ]

    drafting.write_jsonl(output, records)
    loaded = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert loaded == records

    result = subprocess.run(
        [sys.executable, "scripts/evaluation/draft_acceptance_questions.py", "--help"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--source" in result.stdout
