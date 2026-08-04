"""Tests for cloud GPU acceptance orchestration helpers."""

from __future__ import annotations

import json
import subprocess
import sys
import tarfile
from pathlib import Path
from types import SimpleNamespace

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

    assert cloud.default_acceptance_output_dir("runpod") == Path(
        "logs/rag_v1_acceptance/cloud/runpod"
    )
    assert cloud.default_acceptance_output_dir("vast") == Path(
        "logs/rag_v1_acceptance/cloud/vast"
    )
    assert config.acceptance_output_dir == Path("logs/rag_v1_acceptance/cloud/runpod")
    assert cloud.CloudRunConfig(repo_root=tmp_path, provider="vast").acceptance_output_dir == Path(
        "logs/rag_v1_acceptance/cloud/vast"
    )
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

    targeted_config = cloud.CloudRunConfig(
        repo_root=tmp_path,
        question_ids=("amarel_data_transfer", "support_helpdesk"),
        include_full_answer=True,
        max_questions=None,
    )
    acceptance_command = cloud.acceptance_command(targeted_config)
    assert acceptance_command.count("--question-id") == 2
    assert "--include-full-answer" in acceptance_command
    assert "amarel_data_transfer" in acceptance_command
    assert "support_helpdesk" in acceptance_command


def test_cli_defaults_to_provider_specific_output_dir() -> None:
    parser = cloud.build_parser()

    assert parser.parse_args([]).acceptance_output_dir is None
    assert parser.parse_args([]).enable_ui_attachments is False
    assert parser.parse_args(["--enable-ui-attachments"]).enable_ui_attachments is True


def test_cli_max_question_resolution_targets_all_requested_ids() -> None:
    assert (
        cloud._resolve_cli_max_questions(
            full_acceptance=False,
            max_questions=None,
            question_ids=("amarel_login", "support_helpdesk"),
        )
        is None
    )
    assert (
        cloud._resolve_cli_max_questions(
            full_acceptance=False,
            max_questions=None,
            question_ids=(),
        )
        == 3
    )
    assert (
        cloud._resolve_cli_max_questions(
            full_acceptance=False,
            max_questions=2,
            question_ids=("amarel_login", "support_helpdesk"),
        )
        == 2
    )


def test_run_cloud_acceptance_deletes_created_runpod(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    _make_repo(tmp_path)
    deleted: list[str] = []
    account_snapshots = iter(
        [
            {"provider": "runpod", "available": True, "clientBalance": 10.0},
            {"provider": "runpod", "available": True, "clientBalance": 9.875},
        ]
    )
    run_dir = tmp_path / "outputs" / "20260601T120000Z"
    run_dir.mkdir(parents=True)
    acceptance_result = SimpleNamespace(
        run_dir=run_dir,
        summary={
            "run_dir": str(run_dir),
            "results_path": str(run_dir / "results.jsonl"),
            "summary_path": str(run_dir / "summary.json"),
            "report_path": str(run_dir / "report.md"),
            "executed_questions": 2,
            "skipped_questions": 0,
            "pass_count": 2,
            "fail_count": 0,
            "promotion_ready": True,
            "manual_review_question_ids": [],
        },
    )

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
    monkeypatch.setattr(cloud, "run_acceptance_harness", lambda config: acceptance_result)
    monkeypatch.setattr(cloud, "delete_runpod_pod", lambda pod_id: deleted.append(pod_id))
    monkeypatch.setattr(cloud, "provider_account_snapshot", lambda config: next(account_snapshots))
    monkeypatch.setattr(
        cloud,
        "provider_resource_snapshot_for",
        lambda config, *, resource_id: {
            "provider": "runpod",
            "available": True,
            "pod": {"id": resource_id, "gpu": "NVIDIA A40"},
        },
    )

    config = cloud.CloudRunConfig(
        repo_root=tmp_path,
        bundle_path=Path("bundle.tar.gz"),
        question_ids=("amarel_data_transfer", "support_helpdesk"),
        include_full_answer=True,
        ui_attachments_enabled=True,
    )

    assert cloud.run_cloud_acceptance(config) == 0
    assert deleted == ["pod-123"]
    ledger = json.loads((run_dir / "cloud_run_ledger.json").read_text(encoding="utf-8"))
    assert ledger["created_resource_id"] == "pod-123"
    assert ledger["requested_gpu"] == cloud.DEFAULT_RUNPOD_GPU_7B
    assert ledger["estimated_cost_usd"] == 0.125
    assert ledger["estimated_cost_source"] == "balance_delta"
    assert ledger["question_ids"] == ["amarel_data_transfer", "support_helpdesk"]
    assert ledger["include_full_answer"] is True
    assert ledger["ui_attachments_enabled"] is True
    assert ledger["acceptance"]["promotion_ready"] is True
    assert (run_dir / "cloud_run_ledger.md").exists()


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
    assert 'export RAG_UI_ATTACHMENTS_ENABLED="false"' in script

    attachment_script = cloud.remote_bootstrap_script(
        cloud.CloudRunConfig(repo_root=tmp_path, ui_attachments_enabled=True),
        "bundle.tar.gz",
    )

    assert 'export RAG_UI_ATTACHMENTS_ENABLED="true"' in attachment_script


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
