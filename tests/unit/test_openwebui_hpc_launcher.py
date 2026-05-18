"""Contract tests for the local OpenWebUI-to-HPC launcher."""

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "deployment" / "macos" / "run_openwebui_for_hpc.sh"


def test_openwebui_hpc_launcher_is_executable_and_has_valid_bash_syntax() -> None:
    assert os.access(SCRIPT, os.X_OK)
    subprocess.run(["bash", "-n", str(SCRIPT)], check=True)


def test_openwebui_hpc_launcher_help_lists_operator_inputs() -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT), "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "--login-host <host>" in result.stdout
    assert "--gateway-compute-host <host>" in result.stdout
    assert "--gateway-port <port>" in result.stdout
    assert "--local-gateway-port <port>" in result.stdout
    assert "--openwebui-port <port>" in result.stdout
    assert "--mode <docker|native|print>" in result.stdout


def test_openwebui_hpc_launcher_targets_rag_gateway_not_raw_vllm() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "ssh" in content
    assert "-N" in content
    assert "-L" in content
    assert "ExitOnForwardFailure=yes" in content
    assert "/health" in content
    assert "/v1/models" in content
    assert "oarc-rag-v1" in content
    assert "host.docker.internal" in content
    assert "OPENAI_API_BASE_URL" in content
    assert "OPENAI_API_KEY" in content
    assert "raw vLLM" in content
