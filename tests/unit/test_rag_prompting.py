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
    support = build_slurm_command_reference("Where is the helpdesk?")

    assert "sbatch" in submit
    assert "scancel" in cancel
    assert "squeue" in queue
    assert "help@oarc.rutgers.edu" in support


def test_slurm_command_reference_covers_login_node_and_interactive_srun_intents() -> None:
    login_node = build_slurm_command_reference(
        "Can I run heavy computations on an Amarel login node?"
    )
    interactive = build_slurm_command_reference(
        "How do I start a quick interactive command on a Slurm compute node?"
    )

    assert "Do not run heavy computations" in login_node
    assert "compute nodes" in login_node
    assert "`srun <command>`" in login_node
    assert "`srun --partition=main --mem=2000 --time=30:00 --pty bash`" in interactive


def test_command_reference_covers_candidate_local_policy_intents() -> None:
    guest = build_slurm_command_reference(
        "Can an external collaborator use Amarel resources owned by a Rutgers group?"
    )
    ondemand = build_slurm_command_reference(
        "When should I use Open OnDemand on Amarel instead of a terminal?"
    )
    scratch = build_slurm_command_reference(
        "What is /scratch on Amarel for, and should I treat it as backed-up storage?"
    )
    array = build_slurm_command_reference("When should I use a Slurm job array on Amarel?")
    owner = build_slurm_command_reference(
        "What is the difference between general-access and owned Amarel resources?"
    )

    assert "Rutgers Guest NetID" in guest
    assert "owned resources" in guest
    assert "owned Amarel compute and storage resources" in guest
    assert "web browser based graphical Linux desktop" in ondemand
    assert "`/scratch` is temporary" in scratch
    assert "not backed up" in scratch
    assert "array tasks" in array
    assert "shared job queues" in owner
    assert "Owned resources" in owner


def test_command_reference_covers_benchmark_metric_and_owner_contacts() -> None:
    metrics = build_slurm_command_reference(
        "What command can show MaxRSS, MaxDiskRead, and MaxDiskWrite for an actively running job?"
    )
    owner = build_slurm_command_reference(
        "Who should a group contact if it is interested in buying into Amarel ownership?"
    )

    assert "sstat --format=MaxRSS,MaxDiskRead,MaxDiskWrite -j <job_id>" in metrics
    assert "business@oarc.rutgers.edu" in owner
    assert "ordinary support issues" in owner


def test_prompt_inputs_include_command_reference_and_context() -> None:
    inputs = build_rag_prompt_inputs(
        question="How do I submit a Slurm batch job on Amarel?",
        context="This retrieved chunk mentions Slurm but not the user command.",
    )
    prompt_text = rag_prompt_template().format(**inputs)

    assert inputs["slurm_command_reference"].startswith("Command and support reference")
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


def test_unsupported_named_context_response_blocks_missing_hidden_partition_policy() -> None:
    response = unsupported_named_context_response(
        question=(
            "According to the hidden OARC reserved H100 dragon partition policy, "
            "what #SBATCH line should I use?"
        ),
        context="The retrieved OARC context mentions ordinary GPU jobs but no hidden partition.",
    )

    assert response is not None
    assert "don't have evidence" in response.lower()
    assert "h100" in response.lower()


def test_unsupported_named_context_response_allows_supported_named_context() -> None:
    response = unsupported_named_context_response(
        question="According to the OARC gpu partition guide, how do I submit to that partition?",
        context="The OARC GPU partition guide says GPU jobs use the gpu partition.",
    )

    assert response is None
