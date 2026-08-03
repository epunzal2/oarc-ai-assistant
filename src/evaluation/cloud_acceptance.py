"""Cloud GPU acceptance orchestration for the RAG gateway.

The runner is intentionally conservative: it transfers an allowlisted runtime
bundle plus a prebuilt FAISS index, blocks secrets and private ServiceNow data,
and tears down provider-created compute by default after the acceptance run.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tarfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
from typing import Any, Sequence
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_PROVIDER = "runpod"
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
DEFAULT_RUNPOD_IMAGE = "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04"
DEFAULT_RUNPOD_TEMPLATE_ID = "runpod-torch-v280"
DEFAULT_RUNPOD_GPU_7B = "NVIDIA GeForce RTX 4090"
DEFAULT_RUNPOD_GPU_LARGE = "NVIDIA A100 80GB PCIe"
DEFAULT_VAST_IMAGE = "pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime"
DEFAULT_VAST_QUERY_7B = (
    "gpu_name=RTX_4090 num_gpus=1 verified=true direct_port_count>=1 rentable=true"
)
DEFAULT_VAST_QUERY_LARGE = (
    "gpu_name=A100 num_gpus=1 gpu_ram>=40 verified=true direct_port_count>=1 rentable=true"
)
DEFAULT_REMOTE_DIR = "/workspace/oarc-rag-cloud"
DEFAULT_LOCAL_TUNNEL_PORT = 18088
DEFAULT_REMOTE_GATEWAY_PORT = 8088
DEFAULT_REMOTE_VLLM_PORT = 8000
DEFAULT_FAISS_INDEX = "vector_index/faiss_public"
DEFAULT_QUESTIONS_PATH = Path("data/evaluation/acceptance/rag_v1_questions.jsonl")
DEFAULT_ACCEPTANCE_OUTPUT = "logs/rag_v1_acceptance"
DEFAULT_BUNDLE_PATH = Path("runtime/cloud_acceptance/oarc-rag-cloud-bundle.tar.gz")
MANIFEST_NAME = "cloud_transfer_manifest.json"

DEFAULT_TRANSFER_PATHS = (
    "src",
    "scripts",
    "configs",
    "data/evaluation/acceptance",
    "pyproject.toml",
    "uv.lock",
    "README.md",
    "LICENSE",
)

PUBLIC_CORPUS_PATHS = (
    "docs/google_sites_guide",
    "docs/slurm-23.02.7/markdown",
    "docs/corpus/authoritative/rutgers",
)

BLOCKED_TRANSFER_PATTERNS = (
    ".env",
    ".env.*",
    "**/.env",
    "**/.env.*",
    "**/*credential*",
    "**/*secret*",
    "**/*.key",
    "**/*.pem",
    "**/*.p12",
    "**/*.pfx",
    "**/id_ed25519",
    "**/id_rsa",
    ".git/**",
    ".venv/**",
    "**/__pycache__/**",
    ".pytest_cache/**",
    ".ruff_cache/**",
    "docs/servicenow",
    "docs/servicenow/**",
    "logs/**",
    "mlruns/**",
    "models/**",
    "results/**",
    "runtime/**",
    "env_check/**",
    "research/**",
    "tmp/**",
    "todo/**",
    "verification/**",
    "repo_export.out",
    "*.log",
)
SILENT_SKIP_TRANSFER_PATTERNS = (
    "**/__pycache__/**",
    "**/*.pyc",
    ".pytest_cache/**",
    ".ruff_cache/**",
)


@dataclass(frozen=True)
class SSHConnection:
    """SSH connection settings used for transfer, remote setup, and tunneling."""

    target: str
    port: int | None = None
    identity_file: str | None = None

    def ssh_base_args(self) -> list[str]:
        args = ["ssh", *_ssh_noninteractive_options()]
        if self.port is not None:
            args.extend(["-p", str(self.port)])
        if self.identity_file:
            args.extend(["-i", self.identity_file])
        args.append(self.target)
        return args

    def scp_base_args(self) -> list[str]:
        args = ["scp", *_ssh_noninteractive_options()]
        if self.port is not None:
            args.extend(["-P", str(self.port)])
        if self.identity_file:
            args.extend(["-i", self.identity_file])
        return args


@dataclass(frozen=True)
class CloudRunConfig:
    """Operator-configurable cloud acceptance run inputs."""

    repo_root: Path
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL
    faiss_index_path: Path = Path(DEFAULT_FAISS_INDEX)
    bundle_path: Path = DEFAULT_BUNDLE_PATH
    remote_dir: str = DEFAULT_REMOTE_DIR
    local_tunnel_port: int = DEFAULT_LOCAL_TUNNEL_PORT
    remote_gateway_port: int = DEFAULT_REMOTE_GATEWAY_PORT
    remote_vllm_port: int = DEFAULT_REMOTE_VLLM_PORT
    questions_path: Path = DEFAULT_QUESTIONS_PATH
    acceptance_output_dir: Path = Path(DEFAULT_ACCEPTANCE_OUTPUT)
    max_questions: int | None = 3
    max_p95_latency_ms: float = 30_000.0
    max_p95_ttft_ms: float = 15_000.0
    allow_public_corpus: bool = False
    build_index: bool = False
    keep_instance: bool = False
    execute: bool = False
    ssh: SSHConnection | None = None
    run_name: str = field(default_factory=lambda: f"oarc-rag-{_timestamp()}")
    runpod_image: str = DEFAULT_RUNPOD_IMAGE
    runpod_template_id: str | None = DEFAULT_RUNPOD_TEMPLATE_ID
    runpod_gpu: str | None = None
    runpod_container_disk_gb: int = 40
    runpod_terminate_after_hours: int = 3
    vast_image: str = DEFAULT_VAST_IMAGE
    vast_offer_id: int | None = None
    vast_offer_query: str | None = None
    vast_disk_gb: int = 40
    vast_search_limit: int = 1
    dry_run_commands: bool = False

    @property
    def resolved_index_path(self) -> Path:
        path = self.faiss_index_path
        return path if path.is_absolute() else self.repo_root / path

    @property
    def resolved_bundle_path(self) -> Path:
        path = self.bundle_path
        return path if path.is_absolute() else self.repo_root / path


@dataclass(frozen=True)
class TransferManifest:
    """Auditable transfer manifest for a cloud runtime bundle."""

    repo_root: Path
    included_paths: tuple[str, ...]
    blocked_patterns: tuple[str, ...]
    allow_public_corpus: bool
    faiss_index_path: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "repo_root": str(self.repo_root),
            "included_paths": list(self.included_paths),
            "blocked_patterns": list(self.blocked_patterns),
            "allow_public_corpus": self.allow_public_corpus,
            "faiss_index_path": self.faiss_index_path,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }


def _ssh_noninteractive_options() -> list[str]:
    """Return SSH options suitable for short-lived cloud hosts in automation."""

    return [
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ServerAliveInterval=30",
        "-o",
        "ServerAliveCountMax=4",
    ]


@dataclass(frozen=True)
class CloudPlan:
    """Dry-run summary of the selected provider, transfer, and checks."""

    provider: str
    model: str
    gpu: str | None
    bundle_path: str
    remote_dir: str
    transfer_file_count: int
    transfer_bytes: int
    create_command: list[str] | None
    delete_command_template: list[str] | None
    acceptance_command: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "gpu": self.gpu,
            "bundle_path": self.bundle_path,
            "remote_dir": self.remote_dir,
            "transfer_file_count": self.transfer_file_count,
            "transfer_bytes": self.transfer_bytes,
            "create_command": self.create_command,
            "delete_command_template": self.delete_command_template,
            "acceptance_command": self.acceptance_command,
        }


def build_parser() -> argparse.ArgumentParser:
    """Create the cloud acceptance CLI parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Run the RAG gateway acceptance harness on a cloud GPU with a safe "
            "allowlisted transfer bundle."
        )
    )
    parser.add_argument("--provider", choices=("runpod", "vast", "existing"), default=DEFAULT_PROVIDER)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--faiss-index-path", type=Path, default=Path(DEFAULT_FAISS_INDEX))
    parser.add_argument("--bundle-path", type=Path, default=DEFAULT_BUNDLE_PATH)
    parser.add_argument("--remote-dir", default=DEFAULT_REMOTE_DIR)
    parser.add_argument("--local-tunnel-port", type=int, default=DEFAULT_LOCAL_TUNNEL_PORT)
    parser.add_argument("--remote-gateway-port", type=int, default=DEFAULT_REMOTE_GATEWAY_PORT)
    parser.add_argument("--remote-vllm-port", type=int, default=DEFAULT_REMOTE_VLLM_PORT)
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS_PATH)
    parser.add_argument("--acceptance-output-dir", type=Path, default=Path(DEFAULT_ACCEPTANCE_OUTPUT))
    parser.add_argument("--max-questions", type=int, default=3)
    parser.add_argument("--full-acceptance", action="store_true")
    parser.add_argument("--max-p95-latency-ms", type=float, default=30_000.0)
    parser.add_argument("--max-p95-ttft-ms", type=float, default=15_000.0)
    parser.add_argument("--allow-public-corpus", action="store_true")
    parser.add_argument("--build-index", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--keep-instance", action="store_true")
    parser.add_argument("--ssh-target")
    parser.add_argument("--ssh-port", type=int)
    parser.add_argument("--ssh-key")
    parser.add_argument("--runpod-image", default=DEFAULT_RUNPOD_IMAGE)
    parser.add_argument("--runpod-template-id", default=DEFAULT_RUNPOD_TEMPLATE_ID)
    parser.add_argument("--runpod-gpu")
    parser.add_argument("--runpod-container-disk-gb", type=int, default=40)
    parser.add_argument("--runpod-terminate-after-hours", type=int, default=3)
    parser.add_argument("--vast-image", default=DEFAULT_VAST_IMAGE)
    parser.add_argument("--vast-offer-id", type=int)
    parser.add_argument("--vast-offer-query")
    parser.add_argument("--vast-disk-gb", type=int, default=40)
    parser.add_argument("--vast-search-limit", type=int, default=1)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point used by `scripts/evaluation/run_cloud_acceptance.py`."""

    args = build_parser().parse_args(argv)
    repo_root = Path.cwd().resolve()
    ssh = (
        SSHConnection(args.ssh_target, port=args.ssh_port, identity_file=args.ssh_key)
        if args.ssh_target
        else None
    )
    config = CloudRunConfig(
        repo_root=repo_root,
        provider=args.provider,
        model=args.model,
        faiss_index_path=args.faiss_index_path,
        bundle_path=args.bundle_path,
        remote_dir=args.remote_dir,
        local_tunnel_port=args.local_tunnel_port,
        remote_gateway_port=args.remote_gateway_port,
        remote_vllm_port=args.remote_vllm_port,
        questions_path=args.questions,
        acceptance_output_dir=args.acceptance_output_dir,
        max_questions=None if args.full_acceptance else args.max_questions,
        max_p95_latency_ms=args.max_p95_latency_ms,
        max_p95_ttft_ms=args.max_p95_ttft_ms,
        allow_public_corpus=args.allow_public_corpus,
        build_index=args.build_index,
        keep_instance=args.keep_instance,
        execute=args.execute,
        ssh=ssh,
        runpod_image=args.runpod_image,
        runpod_template_id=args.runpod_template_id,
        runpod_gpu=args.runpod_gpu,
        runpod_container_disk_gb=args.runpod_container_disk_gb,
        runpod_terminate_after_hours=args.runpod_terminate_after_hours,
        vast_image=args.vast_image,
        vast_offer_id=args.vast_offer_id,
        vast_offer_query=args.vast_offer_query,
        vast_disk_gb=args.vast_disk_gb,
        vast_search_limit=args.vast_search_limit,
    )
    if config.execute:
        return run_cloud_acceptance(config)
    if config.build_index:
        build_local_faiss_index(config)

    manifest = build_transfer_manifest(config)
    plan = build_cloud_plan(config, manifest)
    print(json.dumps(plan.as_dict(), indent=2, sort_keys=True))
    return 0


def choose_runpod_gpu(model: str) -> str:
    """Return a conservative default GPU for the requested model."""

    lowered = model.lower()
    if any(token in lowered for token in ("14b", "32b", "70b", "mixtral", "gpt-oss-20b")):
        return DEFAULT_RUNPOD_GPU_LARGE
    return DEFAULT_RUNPOD_GPU_7B


def default_vast_offer_query(model: str) -> str:
    """Return the default Vast marketplace query for the requested model."""

    lowered = model.lower()
    if any(token in lowered for token in ("14b", "32b", "70b", "mixtral", "gpt-oss-20b")):
        return DEFAULT_VAST_QUERY_LARGE
    return DEFAULT_VAST_QUERY_7B


def build_transfer_manifest(config: CloudRunConfig) -> TransferManifest:
    """Build and validate the allowlisted transfer manifest."""

    repo_root = config.repo_root.resolve()
    include_roots: list[Path] = [repo_root / path for path in DEFAULT_TRANSFER_PATHS]
    include_roots.append(config.resolved_index_path)
    if config.allow_public_corpus:
        include_roots.extend(repo_root / path for path in PUBLIC_CORPUS_PATHS)

    included: list[str] = []
    for root in include_roots:
        if not root.exists():
            if root == config.resolved_index_path:
                raise FileNotFoundError(
                    f"FAISS index path does not exist: {config.resolved_index_path}"
                )
            continue
        included.extend(_iter_relative_files(repo_root, root))

    unique = tuple(sorted({path for path in included if not _is_silent_skip(path)}))
    blocked = blocked_transfer_paths(unique)
    if blocked:
        detail = ", ".join(blocked[:8])
        raise ValueError(f"blocked transfer path(s) selected: {detail}")
    if not any(path.startswith(_rel_posix(repo_root, config.resolved_index_path)) for path in unique):
        raise ValueError(f"FAISS index path has no files: {config.resolved_index_path}")

    return TransferManifest(
        repo_root=repo_root,
        included_paths=unique,
        blocked_patterns=BLOCKED_TRANSFER_PATTERNS,
        allow_public_corpus=config.allow_public_corpus,
        faiss_index_path=_rel_posix(repo_root, config.resolved_index_path),
    )


def blocked_transfer_paths(paths: Sequence[str]) -> list[str]:
    """Return transfer paths that match secret/private/generated block rules."""

    blocked: list[str] = []
    for path in paths:
        normalized = str(PurePosixPath(path))
        if any(_matches_pattern(normalized, pattern) for pattern in BLOCKED_TRANSFER_PATTERNS):
            blocked.append(normalized)
    return blocked


def create_transfer_bundle(config: CloudRunConfig, manifest: TransferManifest) -> Path:
    """Write the compressed tar bundle described by `manifest`."""

    bundle = config.resolved_bundle_path
    bundle.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(bundle, "w:gz") as archive:
        for rel_path in manifest.included_paths:
            archive.add(config.repo_root / rel_path, arcname=rel_path, recursive=False)
        manifest_bytes = json.dumps(manifest.as_dict(), indent=2, sort_keys=True).encode("utf-8")
        info = tarfile.TarInfo(MANIFEST_NAME)
        info.size = len(manifest_bytes)
        info.mtime = int(time.time())
        archive.addfile(info, io.BytesIO(manifest_bytes))
    return bundle


def build_cloud_plan(config: CloudRunConfig, manifest: TransferManifest) -> CloudPlan:
    """Return a dry-run plan without provider or network side effects."""

    transfer_bytes = sum((config.repo_root / rel_path).stat().st_size for rel_path in manifest.included_paths)
    gpu = None
    create_command = None
    delete_template = None
    if config.provider == "runpod":
        gpu = config.runpod_gpu or choose_runpod_gpu(config.model)
        create_command = runpod_create_command(config, gpu)
        delete_template = ["runpodctl", "pod", "delete", "<pod-id>"]
    elif config.provider == "vast":
        gpu = config.vast_offer_query or default_vast_offer_query(config.model)
        create_command = (
            vast_create_command(config, config.vast_offer_id)
            if config.vast_offer_id is not None
            else vast_search_command(config)
        )
        delete_template = ["vastai", "destroy", "instance", "<instance-id>", "--raw"]
    return CloudPlan(
        provider=config.provider,
        model=config.model,
        gpu=gpu,
        bundle_path=str(config.resolved_bundle_path),
        remote_dir=config.remote_dir,
        transfer_file_count=len(manifest.included_paths),
        transfer_bytes=transfer_bytes,
        create_command=create_command,
        delete_command_template=delete_template,
        acceptance_command=acceptance_command(config),
    )


def run_cloud_acceptance(config: CloudRunConfig) -> int:
    """Execute the cloud acceptance workflow and always clean up created compute."""

    if config.build_index:
        build_local_faiss_index(config)
    manifest = build_transfer_manifest(config)
    bundle = create_transfer_bundle(config, manifest)
    created_resource_id: str | None = None
    ssh = config.ssh
    try:
        if config.provider == "runpod" and ssh is None:
            created_resource_id = create_runpod_pod(config)
            ssh = get_runpod_ssh_connection(created_resource_id)
        elif config.provider == "vast" and ssh is None:
            created_resource_id = create_vast_instance(config)
            ssh = get_vast_ssh_connection(created_resource_id)
        if ssh is None:
            raise ValueError("--ssh-target is required for provider=existing")

        transfer_bundle(ssh, bundle, config.remote_dir)
        bootstrap_remote_runtime(ssh, config, bundle.name)
        tunnel = open_tunnel(ssh, config)
        try:
            wait_for_local_gateway(config)
            prewarm_gateway_completion(config)
            return run_acceptance_harness(config)
        finally:
            tunnel.terminate()
            try:
                tunnel.wait(timeout=10)
            except subprocess.TimeoutExpired:
                tunnel.kill()
    finally:
        if created_resource_id and not config.keep_instance:
            if config.provider == "runpod":
                delete_runpod_pod(created_resource_id)
            elif config.provider == "vast":
                delete_vast_instance(created_resource_id)


def build_local_faiss_index(config: CloudRunConfig) -> None:
    """Build the public FAISS index locally before packaging."""

    data_path = os.pathsep.join(PUBLIC_CORPUS_PATHS)
    env = {
        **os.environ,
        "DATA_PATH": data_path,
        "EMBEDDING_DEVICE": "cpu",
        "SERVICE_NOW_DATA_PATH": "/dev/null",
    }
    cmd = [
        sys.executable,
        "scripts/rag/create_vector_store.py",
        "--vector-store",
        "faiss",
        "--persist-dir",
        str(config.resolved_index_path),
        "--servicenow-path",
        "/dev/null",
    ]
    run_checked(cmd, cwd=config.repo_root, env=env)


def runpod_create_command(config: CloudRunConfig, gpu: str | None = None) -> list[str]:
    """Return the documented `runpodctl pod create` command."""

    command = [
        "runpodctl",
        "pod",
        "create",
        "--name",
        config.run_name,
        "--gpu-id",
        gpu or config.runpod_gpu or choose_runpod_gpu(config.model),
        "--container-disk-in-gb",
        str(config.runpod_container_disk_gb),
        "--ports",
        "22/tcp",
    ]
    if config.runpod_template_id:
        command.extend(["--template-id", config.runpod_template_id])
    else:
        command.extend(["--image", config.runpod_image])
    if config.runpod_terminate_after_hours > 0:
        command.extend(
            [
                "--terminate-after",
                _future_utc_iso(hours=config.runpod_terminate_after_hours),
            ]
        )
    return command


def create_runpod_pod(config: CloudRunConfig) -> str:
    """Create a RunPod pod and return its ID."""

    result = run_checked(runpod_create_command(config), cwd=config.repo_root)
    pod_id = _extract_runpod_pod_id(result.stdout)
    if not pod_id:
        raise RuntimeError("runpodctl pod create did not return a pod id")
    return pod_id


def delete_runpod_pod(pod_id: str) -> None:
    """Terminate a RunPod pod; errors are surfaced to the caller."""

    run_checked(["runpodctl", "pod", "delete", pod_id], cwd=Path.cwd())


def get_runpod_ssh_connection(
    pod_id: str,
    *,
    timeout_s: int = 900,
    poll_s: int = 15,
) -> SSHConnection:
    """Wait for RunPod SSH connection info and parse it into SSH arguments."""

    deadline = time.monotonic() + timeout_s
    last_output = ""
    while time.monotonic() < deadline:
        result = run_checked(["runpodctl", "ssh", "info", pod_id], cwd=Path.cwd())
        last_output = result.stdout
        try:
            return parse_ssh_command(result.stdout)
        except ValueError as exc:
            if not _runpod_ssh_info_not_ready(result.stdout):
                raise exc
        time.sleep(poll_s)
    raise TimeoutError(
        f"timed out waiting for RunPod SSH info for {pod_id}; last output={last_output[:160]}"
    )


def _runpod_ssh_info_not_ready(output: str) -> bool:
    """Return true for RunPod SSH info responses that mean the Pod is still booting."""

    lowered = output.lower()
    return "pod not ready" in lowered or '"status": "running"' in lowered


def vast_search_command(config: CloudRunConfig) -> list[str]:
    """Return the documented Vast offer-search command used for auto-selection."""

    return [
        "vastai",
        "search",
        "offers",
        "--raw",
        "--limit",
        str(config.vast_search_limit),
        config.vast_offer_query or default_vast_offer_query(config.model),
        "-o",
        "dlperf_usd-",
    ]


def vast_create_command(config: CloudRunConfig, offer_id: int | None) -> list[str]:
    """Return the documented Vast instance-create command."""

    if offer_id is None:
        raise ValueError("offer_id is required to build a Vast create command")
    return [
        "vastai",
        "create",
        "instance",
        str(offer_id),
        "--image",
        config.vast_image,
        "--disk",
        str(config.vast_disk_gb),
        "--ssh",
        "--direct",
        "--onstart-cmd",
        "sleep infinity",
        "--raw",
    ]


def create_vast_instance(config: CloudRunConfig) -> str:
    """Create a Vast instance and return its instance ID."""

    offer_id = config.vast_offer_id
    if offer_id is None:
        search = run_checked(vast_search_command(config), cwd=config.repo_root)
        offer_id = _extract_vast_offer_id(search.stdout)
    if offer_id is None:
        raise RuntimeError("vastai search offers did not return an offer id")

    result = run_checked(vast_create_command(config, offer_id), cwd=config.repo_root)
    instance_id = _extract_vast_instance_id(result.stdout)
    if instance_id is None:
        raise RuntimeError("vastai create instance did not return an instance id")
    wait_for_vast_instance(instance_id, config.repo_root)
    return str(instance_id)


def wait_for_vast_instance(instance_id: str, repo_root: Path, *, timeout_s: int = 600) -> None:
    """Wait for a Vast instance to report `running` before SSH discovery."""

    deadline = time.monotonic() + timeout_s
    last_status = "unknown"
    while time.monotonic() < deadline:
        result = run_checked(["vastai", "show", "instance", instance_id, "--raw"], cwd=repo_root)
        last_status = _extract_status(result.stdout) or last_status
        if last_status == "running":
            return
        if last_status in {"exited", "offline", "unknown"}:
            raise RuntimeError(f"vastai instance {instance_id} entered terminal status {last_status}")
        time.sleep(15)
    raise TimeoutError(f"timed out waiting for vastai instance {instance_id}; last status={last_status}")


def get_vast_ssh_connection(instance_id: str) -> SSHConnection:
    """Read Vast SSH connection info and parse it into SSH arguments."""

    result = run_checked(["vastai", "ssh-url", instance_id], cwd=Path.cwd())
    return parse_ssh_command(result.stdout)


def delete_vast_instance(instance_id: str) -> None:
    """Destroy a Vast instance so provider billing stops."""

    run_checked(["vastai", "destroy", "instance", instance_id, "--raw"], cwd=Path.cwd())


def parse_ssh_command(output: str) -> SSHConnection:
    """Parse a provider-printed `ssh user@host -p port -i key` command."""

    json_command = _json_ssh_command(output)
    if json_command:
        output = json_command

    url_match = re.search(r"ssh://[^\s]+", output)
    if url_match:
        parsed = urlparse(url_match.group(0))
        if parsed.hostname and parsed.username:
            return SSHConnection(
                target=f"{parsed.username}@{parsed.hostname}",
                port=parsed.port,
            )

    match = re.search(r"\bssh\s+(.+)", output)
    raw = match.group(0) if match else output.strip()
    parts = shlex.split(raw)
    if not parts or parts[0] != "ssh":
        raise ValueError(f"could not parse ssh command from output: {output[:120]}")
    target: str | None = None
    port: int | None = None
    identity_file: str | None = None
    index = 1
    while index < len(parts):
        token = parts[index]
        if token == "-p" and index + 1 < len(parts):
            port = int(parts[index + 1])
            index += 2
            continue
        if token == "-i" and index + 1 < len(parts):
            identity_file = parts[index + 1]
            index += 2
            continue
        if not token.startswith("-") and target is None:
            target = token
        index += 1
    if not target:
        raise ValueError(f"ssh target missing from output: {output[:120]}")
    return SSHConnection(target=target, port=port, identity_file=identity_file)


def _json_ssh_command(output: str) -> str | None:
    """Return a provider JSON `ssh_command` field when present."""

    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    for key in ("ssh_command", "sshCommand", "ssh"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def transfer_bundle(ssh: SSHConnection, bundle: Path, remote_dir: str) -> None:
    """Copy the audited bundle to the remote host using SSH/SCP."""

    run_checked(ssh.ssh_base_args() + ["mkdir", "-p", remote_dir], cwd=bundle.parent)
    remote_path = f"{ssh.target}:{_remote_join(remote_dir, bundle.name)}"
    run_checked(ssh.scp_base_args() + [str(bundle), remote_path], cwd=bundle.parent)


def bootstrap_remote_runtime(ssh: SSHConnection, config: CloudRunConfig, bundle_name: str) -> None:
    """Extract the bundle and start vLLM plus the RAG gateway on loopback."""

    script = remote_bootstrap_script(config, bundle_name)
    run_checked(ssh.ssh_base_args() + ["bash", "-se"], cwd=config.repo_root, input_text=script)


def remote_bootstrap_script(config: CloudRunConfig, bundle_name: str) -> str:
    """Return the remote setup script used after transfer."""

    rel_index = _rel_posix(config.repo_root, config.resolved_index_path)
    return f"""\
set -euo pipefail
cd {shlex.quote(config.remote_dir)}
tar -xzf {shlex.quote(bundle_name)}
mkdir -p logs runtime
if ! command -v uv >/dev/null 2>&1; then
  python3 -m pip install --user uv
  export PATH="$HOME/.local/bin:$PATH"
fi
uv sync --extra dev --extra vllm
uv pip install 'transformers>=4.48.2,<5'
pkill -f 'vllm serve {shlex.quote(config.model)}' >/dev/null 2>&1 || true
pkill -f 'uvicorn src.rag.api:app' >/dev/null 2>&1 || true
nohup uv run --no-sync vllm serve {shlex.quote(config.model)} \
  --host 127.0.0.1 \
  --port {config.remote_vllm_port} \
  > logs/vllm.log 2>&1 &
for _ in $(seq 1 120); do
  if curl -fsS http://127.0.0.1:{config.remote_vllm_port}/health >/dev/null 2>&1; then
    break
  fi
  sleep 5
done
export PYTHONPATH="$PWD"
export DATA_PATH=""
export SERVICE_NOW_DATA_PATH="/dev/null"
export FAISS_INDEX_PATH={shlex.quote(rel_index)}
export RAG_GATEWAY_LLM_PROVIDER="vllm"
export RAG_GATEWAY_VECTOR_STORE="faiss"
export RAG_RETRIEVAL_MODE="vector"
export RAG_UI_ATTACHMENTS_ENABLED="false"
export VLLM_BASE_URL="http://127.0.0.1:{config.remote_vllm_port}"
export VLLM_HEALTH_URL="http://127.0.0.1:{config.remote_vllm_port}/health"
export VLLM_MODEL={shlex.quote(config.model)}
export VLLM_TIMEOUT="120"
export VLLM_MAX_RETRIES="2"
nohup uv run --no-sync uvicorn src.rag.api:app \
  --host 127.0.0.1 \
  --port {config.remote_gateway_port} \
  > logs/gateway.log 2>&1 &
for _ in $(seq 1 60); do
  if curl -fsS http://127.0.0.1:{config.remote_gateway_port}/health >/dev/null 2>&1; then
    exit 0
  fi
  sleep 2
done
echo "RAG gateway did not become healthy; inspect logs/gateway.log and logs/vllm.log" >&2
exit 1
"""


def open_tunnel(ssh: SSHConnection, config: CloudRunConfig) -> subprocess.Popen[str]:
    """Open a local SSH tunnel to the remote loopback gateway."""

    cmd = ssh.ssh_base_args()
    target = cmd.pop()
    cmd.extend(
        [
            "-N",
            "-L",
            f"127.0.0.1:{config.local_tunnel_port}:127.0.0.1:{config.remote_gateway_port}",
            target,
        ]
    )
    return subprocess.Popen(cmd, cwd=config.repo_root, text=True)  # noqa: S603


def wait_for_local_gateway(config: CloudRunConfig, *, timeout_s: int = 30) -> None:
    """Wait until the local SSH tunnel can reach the gateway health endpoint."""

    url = f"http://127.0.0.1:{config.local_tunnel_port}/health"
    deadline = time.monotonic() + timeout_s
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=2) as response:  # noqa: S310
                if 200 <= response.status < 500:
                    return
        except (OSError, URLError) as exc:
            last_error = exc
        time.sleep(0.5)
    detail = f": {last_error}" if last_error else ""
    raise TimeoutError(f"timed out waiting for local gateway tunnel at {url}{detail}")


def prewarm_gateway_completion(config: CloudRunConfig, *, timeout_s: int = 120) -> None:
    """Run one direct tunneled completion before the measured acceptance questions."""

    url = f"http://127.0.0.1:{config.local_tunnel_port}/v1/chat/completions"
    payload = {
        "model": "oarc-rag-v1",
        "messages": [
            {
                "role": "user",
                "content": "Readiness check: answer with one short sentence that includes the word ready.",
            }
        ],
        "max_tokens": 24,
        "stream": False,
        "temperature": 0,
    }
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout_s) as response:  # noqa: S310
        if not 200 <= response.status < 300:
            raise RuntimeError(f"gateway prewarm failed with HTTP {response.status}")


def run_acceptance_harness(config: CloudRunConfig) -> int:
    """Run the existing local acceptance harness against the SSH tunnel."""

    from src.evaluation.acceptance import main as acceptance_main

    return acceptance_main(acceptance_command(config)[2:])


def acceptance_command(config: CloudRunConfig) -> list[str]:
    """Return the local acceptance harness command."""

    command = [
        "python",
        "scripts/evaluation/run_v1_acceptance.py",
        "--base-url",
        f"http://127.0.0.1:{config.local_tunnel_port}/v1",
        "--output-dir",
        str(config.acceptance_output_dir),
        "--questions",
        str(config.questions_path),
        "--max-p95-latency-ms",
        str(config.max_p95_latency_ms),
        "--max-p95-ttft-ms",
        str(config.max_p95_ttft_ms),
    ]
    if config.max_questions is not None:
        command.extend(["--max-questions", str(config.max_questions)])
    return command


def run_checked(
    cmd: Sequence[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a command with captured output and sanitized failure text."""

    result = subprocess.run(  # noqa: S603
        list(cmd),
        cwd=cwd,
        env=env,
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = _sanitize_process_text(result.stderr)
        stdout = _sanitize_process_text(result.stdout)
        raise RuntimeError(
            f"command failed ({result.returncode}): {shlex.join(cmd)}\n"
            f"stdout: {stdout[:1000]}\nstderr: {stderr[:1000]}"
        )
    return result


def _extract_runpod_pod_id(output: str) -> str | None:
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict):
        for key in ("id", "pod_id", "podId", "containerId"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
        data = payload.get("data")
        if isinstance(data, dict):
            for key in ("id", "pod_id", "podId", "containerId"):
                value = data.get(key)
                if isinstance(value, str) and value:
                    return value
    match = re.search(r"\bpod[_-]?id\b\W+([A-Za-z0-9_-]+)", output, flags=re.IGNORECASE)
    return match.group(1) if match else None


def _extract_vast_offer_id(output: str) -> int | None:
    payload = _parse_jsonish(output)
    records = payload if isinstance(payload, list) else None
    if isinstance(payload, dict):
        data = payload.get("data")
        records = data if isinstance(data, list) else [payload]
    if records:
        first = records[0]
        if isinstance(first, dict):
            for key in ("id", "offer_id", "ask_contract_id"):
                value = first.get(key)
                if isinstance(value, int):
                    return value
                if isinstance(value, str) and value.isdigit():
                    return int(value)
    match = re.search(r"^\s*(\d+)\b", output, flags=re.MULTILINE)
    return int(match.group(1)) if match else None


def _extract_vast_instance_id(output: str) -> int | None:
    payload = _parse_jsonish(output)
    if isinstance(payload, dict):
        for key in ("new_contract", "id", "instance_id", "contract_id"):
            value = payload.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, str) and value.isdigit():
                return int(value)
    match = re.search(r"\b(?:new_contract|instance[_ -]?id)\b\W+(\d+)", output, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def _extract_status(output: str) -> str | None:
    payload = _parse_jsonish(output)
    records: list[Any]
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        data = payload.get("instances") or payload.get("data")
        records = data if isinstance(data, list) else [payload]
    else:
        records = []
    for record in records:
        if isinstance(record, dict):
            status = record.get("status") or record.get("actual_status")
            if isinstance(status, str):
                return status.lower()
    match = re.search(r"\b(?:status|actual_status)\b\W+([A-Za-z_-]+)", output, flags=re.IGNORECASE)
    return match.group(1).lower() if match else None


def _parse_jsonish(output: str) -> Any:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return None


def _iter_relative_files(repo_root: Path, root: Path) -> list[str]:
    root = root.resolve()
    if root.is_file():
        return [_rel_posix(repo_root, root)]
    return [
        _rel_posix(repo_root, path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]


def _rel_posix(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _matches_pattern(path: str, pattern: str) -> bool:
    return fnmatch(path, pattern) or fnmatch(f"./{path}", pattern)


def _is_silent_skip(path: str) -> bool:
    normalized = str(PurePosixPath(path))
    return any(_matches_pattern(normalized, pattern) for pattern in SILENT_SKIP_TRANSFER_PATTERNS)


def _remote_join(remote_dir: str, filename: str) -> str:
    return f"{remote_dir.rstrip('/')}/{filename}"


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _future_utc_iso(*, hours: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sanitize_process_text(text: str) -> str:
    value = text or ""
    value = re.sub(
        r"(?i)\b((?:RUNPOD|VAST|VLLM|HF|HUGGINGFACE)_API_KEY)\s*[:=]\s*[^\s,;]+",
        r"\1=[redacted]",
        value,
    )
    value = re.sub(r"(?i)\b(Bearer|token|api[_-]?key)\s+[A-Za-z0-9._~+/=-]{8,}", r"\1 [redacted]", value)
    return value


if __name__ == "__main__":
    raise SystemExit(main())
