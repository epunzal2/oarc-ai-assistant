"""Tests for cloud GPU acceptance orchestration helpers."""

from __future__ import annotations

import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from src.evaluation import cloud_acceptance as cloud

ROOT = Path(__file__).resolve().parents[2]


def _make_repo(root: Path) -> None:
    (root / "src").mkdir()
    (root / "src" / "placeholder.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "data/evaluation/acceptance").mkdir(parents=True)
    (root / "data/evaluation/acceptance/rag_v1_questions.jsonl").write_text(
        '{"id": "q1", "category": "slurm_basics", "question": "How do I submit?"}\n',
        encoding="utf-8",
    )
    (root / "vector_index/faiss_public").mkdir(parents=True)
    (root / "vector_index/faiss_public/index.faiss").write_text("faiss", encoding="utf-8")
    (root / "vector_index/faiss_public/index.pkl").write_text("pickle", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname='test'\n", encoding="utf-8")
    (root / "README.md").write_text("# Test\n", encoding="utf-8")
    (root / "LICENSE").write_text("test\n", encoding="utf-8")


def test_transfer_manifest_blocks_secret_and_servicenow_paths(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / ".env").write_text("RUNPOD_API_KEY=secret\n", encoding="utf-8")
    config = cloud.CloudRunConfig(repo_root=tmp_path)

    with pytest.raises(ValueError, match="blocked transfer path"):
        cloud.build_transfer_manifest(config)

    assert cloud.blocked_transfer_paths(["docs/servicenow/task123.json", ".env"]) == [
        "docs/servicenow/task123.json",
        ".env",
    ]


def test_transfer_bundle_contains_only_allowlisted_files_and_manifest(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    config = cloud.CloudRunConfig(repo_root=tmp_path, bundle_path=Path("bundle.tar.gz"))
    manifest = cloud.build_transfer_manifest(config)

    bundle = cloud.create_transfer_bundle(config, manifest)

    with tarfile.open(bundle, "r:gz") as archive:
        names = set(archive.getnames())
        manifest_file = archive.extractfile(cloud.MANIFEST_NAME)
        assert manifest_file is not None
        manifest_payload = json.loads(manifest_file.read().decode("utf-8"))

    assert "vector_index/faiss_public/index.faiss" in names
    assert cloud.MANIFEST_NAME in names
    assert not any(name.endswith(".env") for name in names)
    assert manifest_payload["faiss_index_path"] == "vector_index/faiss_public"


def test_provider_command_defaults_and_parsers(tmp_path: Path) -> None:
    config = cloud.CloudRunConfig(repo_root=tmp_path, model="Qwen/Qwen2.5-7B-Instruct")

    assert cloud.choose_runpod_gpu(config.model) == cloud.DEFAULT_RUNPOD_GPU_7B
    assert cloud.choose_runpod_gpu("Qwen/Qwen2.5-32B-Instruct") == cloud.DEFAULT_RUNPOD_GPU_LARGE
    assert "RTX_4090" in cloud.default_vast_offer_query(config.model)
    assert "A100" in cloud.default_vast_offer_query("Qwen/Qwen2.5-32B-Instruct")
    runpod_command = cloud.runpod_create_command(config)
    assert runpod_command[:3] == ["runpodctl", "pod", "create"]
    assert "--template-id" in runpod_command
    assert cloud.DEFAULT_RUNPOD_TEMPLATE_ID in runpod_command
    assert "--ports" in runpod_command
    assert "22/tcp" in runpod_command
    assert "--terminate-after" in runpod_command
    image_config = cloud.CloudRunConfig(repo_root=tmp_path, runpod_template_id=None)
    image_command = cloud.runpod_create_command(image_config)
    assert "--image" in image_command
    assert cloud.DEFAULT_RUNPOD_IMAGE in image_command
    assert cloud.vast_search_command(config)[:4] == ["vastai", "search", "offers", "--raw"]
    assert cloud.vast_create_command(config, 12345)[:4] == [
        "vastai",
        "create",
        "instance",
        "12345",
    ]
    assert cloud._extract_runpod_pod_id('{"id": "pod-123"}') == "pod-123"
    assert cloud._extract_vast_offer_id('[{"id": 111, "dph": 0.4}]') == 111
    assert cloud._extract_vast_instance_id('{"success": true, "new_contract": 222}') == 222
    assert cloud._extract_status('{"status": "running"}') == "running"

    ssh = cloud.parse_ssh_command("ssh root@example.com -p 22022 -i /tmp/key")
    assert ssh.target == "root@example.com"
    assert ssh.port == 22022
    assert ssh.identity_file == "/tmp/key"

    ssh_url = cloud.parse_ssh_command("ssh://root@203.0.113.10:22022")
    assert ssh_url.target == "root@203.0.113.10"
    assert ssh_url.port == 22022

    ssh_json = cloud.parse_ssh_command(
        json.dumps(
            {
                "ssh_command": "ssh -i /tmp/runpod-key root@203.0.113.20 -p 22081",
            }
        )
    )
    assert ssh_json.target == "root@203.0.113.20"
    assert ssh_json.port == 22081
    assert ssh_json.identity_file == "/tmp/runpod-key"


def test_run_cloud_acceptance_deletes_created_runpod(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _make_repo(tmp_path)
    deleted: list[str] = []

    class FakeTunnel:
        def terminate(self) -> None:
            pass

        def wait(self, timeout: int) -> None:
            pass

        def kill(self) -> None:
            pass

    monkeypatch.setattr(cloud, "create_runpod_pod", lambda config: "pod-123")
    monkeypatch.setattr(
        cloud,
        "get_runpod_ssh_connection",
        lambda pod_id: cloud.SSHConnection("root@example.com", port=22022),
    )
    monkeypatch.setattr(cloud, "transfer_bundle", lambda ssh, bundle, remote_dir: None)
    monkeypatch.setattr(cloud, "bootstrap_remote_runtime", lambda ssh, config, bundle_name: None)
    monkeypatch.setattr(cloud, "open_tunnel", lambda ssh, config: FakeTunnel())
    monkeypatch.setattr(cloud, "wait_for_local_gateway", lambda config: None)
    monkeypatch.setattr(cloud, "prewarm_gateway_completion", lambda config: None)
    monkeypatch.setattr(cloud, "run_acceptance_harness", lambda config: 0)
    monkeypatch.setattr(cloud, "delete_runpod_pod", lambda pod_id: deleted.append(pod_id))

    config = cloud.CloudRunConfig(repo_root=tmp_path, bundle_path=Path("bundle.tar.gz"))

    assert cloud.run_cloud_acceptance(config) == 0
    assert deleted == ["pod-123"]


def test_get_runpod_ssh_connection_waits_until_ready(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outputs = iter(
        [
            subprocess.CompletedProcess(
                ["runpodctl", "ssh", "info", "pod-123"],
                0,
                stdout='{"error": "pod not ready", "status": "RUNNING"}',
                stderr="",
            ),
            subprocess.CompletedProcess(
                ["runpodctl", "ssh", "info", "pod-123"],
                0,
                stdout="ssh root@example.com -p 22022",
                stderr="",
            ),
        ]
    )
    sleeps: list[int] = []

    monkeypatch.setattr(cloud, "run_checked", lambda *args, **kwargs: next(outputs))
    monkeypatch.setattr(cloud.time, "sleep", lambda seconds: sleeps.append(seconds))

    ssh = cloud.get_runpod_ssh_connection("pod-123", timeout_s=60, poll_s=5)

    assert ssh.target == "root@example.com"
    assert ssh.port == 22022
    assert sleeps == [5]


def test_remote_bootstrap_pins_vllm_transformers_compatibility(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    config = cloud.CloudRunConfig(repo_root=tmp_path)

    script = cloud.remote_bootstrap_script(config, "bundle.tar.gz")

    assert "uv sync --extra dev --extra vllm" in script
    assert "uv pip install 'transformers>=4.48.2,<5'" in script
    assert "uv run --no-sync vllm serve" in script
    assert "uv run --no-sync uvicorn" in script


def test_cloud_acceptance_wrapper_help() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/evaluation/run_cloud_acceptance.py", "--help"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--provider" in result.stdout
