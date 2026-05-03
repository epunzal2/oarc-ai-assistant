"""Contract tests for hosted vLLM HPC launcher scripts."""

from pathlib import Path


HPC_SCRIPT_DIR = Path("scripts/deployment/hpc")


def test_vllm_serve_sbatch_writes_endpoint_metadata() -> None:
    content = (HPC_SCRIPT_DIR / "vllm_serve.sbatch").read_text(encoding="utf-8")

    assert "vllm-endpoint.json" in content
    assert '"health_url"' in content
    assert "vllm serve" in content
    assert "/health" in content


def test_submit_vllm_serve_supports_endpoint_dir() -> None:
    content = (HPC_SCRIPT_DIR / "submit_vllm_serve.sh").read_text(encoding="utf-8")

    assert "--endpoint-dir <path>" in content
    assert 'export VLLM_ENDPOINT_DIR="${ENDPOINT_DIR}"' in content
    assert "Generated VLLM_API_KEY" in content


def test_remote_chat_launcher_does_not_require_llama_cpp_model() -> None:
    content = (HPC_SCRIPT_DIR / "run_chat_hpc_remote.sbatch").read_text(encoding="utf-8")

    assert "LLAMA_CPP_MODEL_PATH" not in content
    assert 'LLM_PROVIDER="${LLM_PROVIDER:-vllm}"' in content
    assert "python -m scripts.deployment.hpc.chat_hpc" in content


def test_hpc_vllm_scripts_use_repo_local_venv() -> None:
    for script_name in (
        "run_chat_hpc.sbatch",
        "run_chat_hpc_remote.sbatch",
        "vllm_serve.sbatch",
    ):
        content = (HPC_SCRIPT_DIR / script_name).read_text(encoding="utf-8")
        assert "scripts/common/activate_project_env.sh" in content
        assert "conda activate" not in content
