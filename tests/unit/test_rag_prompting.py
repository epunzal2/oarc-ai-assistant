"""Tests for small-model RAG prompt grounding helpers."""

from __future__ import annotations

from src.rag.prompting import (
    build_rag_prompt_inputs,
    build_slurm_command_reference,
    rag_prompt_template,
    unsupported_named_context_response,
)


def test_slurm_command_reference_covers_acceptance_smoke_intents() -> None:
    submit = build_slurm_command_reference("How do I submit a Slurm batch job on Amarel?")
    cancel = build_slurm_command_reference("How do I cancel a running Slurm job?")
    queue = build_slurm_command_reference("What command checks my queued or running jobs?")

    assert "sbatch" in submit
    assert "scancel" in cancel
    assert "squeue" in queue
    assert build_slurm_command_reference("Where is the helpdesk?") == "No command reference."


def test_prompt_inputs_include_command_reference_and_context() -> None:
    inputs = build_rag_prompt_inputs(
        question="How do I submit a Slurm batch job on Amarel?",
        context="This retrieved chunk mentions Slurm but not the user command.",
    )
    prompt_text = rag_prompt_template().format(**inputs)

    assert inputs["slurm_command_reference"].startswith("Slurm command reference")
    assert "`sbatch <job_script.sh>`" in prompt_text
    assert "Answer with the exact command first" in prompt_text
    assert "This retrieved chunk mentions Slurm" in prompt_text


def test_unsupported_named_context_response_blocks_missing_partition_guide() -> None:
    response = unsupported_named_context_response(
        question=(
            "According to the OARC quantum dragon partition guide, "
            "how do I submit to that partition?"
        ),
        context="Submit ordinary Slurm jobs with sbatch. Check OARC docs for real partitions.",
    )

    assert response is not None
    assert "don't have evidence" in response.lower()
    assert "helpdesk" in response.lower()
    assert "#SBATCH --partition=quantum-dragon" not in response


def test_unsupported_named_context_response_allows_supported_named_context() -> None:
    response = unsupported_named_context_response(
        question="According to the OARC gpu partition guide, how do I submit to that partition?",
        context="The OARC GPU partition guide says GPU jobs use the gpu partition.",
    )

    assert response is None
