"""Contract tests for repo-local environment setup scripts."""

from pathlib import Path


def test_setup_hpc_uses_uv_sync_and_not_conda() -> None:
    content = Path("scripts/deployment/hpc/setup_hpc.sh").read_text(encoding="utf-8")

    assert "uv sync" in content
    assert ".venv" in content
    assert "conda activate" not in content


def test_setup_local_uses_uv_sync() -> None:
    content = Path("scripts/deployment/macos/setup_local.sh").read_text(encoding="utf-8")

    assert "uv sync" in content
    assert "uv pip install -r requirements.txt" not in content
