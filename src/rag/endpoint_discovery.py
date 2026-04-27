from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional

_ENDPOINT_FILENAME = "vllm-endpoint.json"


@dataclass(frozen=True)
class EndpointInfo:
    """Endpoint metadata published by a running HPC vLLM job."""

    base_url: str
    health_url: str
    model: str
    node: str
    port: int
    slurm_job_id: str
    started_at: str
    api_key_required: bool


def resolve_endpoint_dir(environ: Optional[Mapping[str, str]] = None) -> Optional[Path]:
    env = environ if environ is not None else os.environ
    raw_value = env.get("VLLM_ENDPOINT_DIR")
    if raw_value is None or raw_value == "":
        return None
    return Path(raw_value).expanduser()


def read_endpoint(endpoint_dir: str | Path) -> Optional[EndpointInfo]:
    endpoint_path = Path(endpoint_dir) / _ENDPOINT_FILENAME
    if not endpoint_path.exists():
        return None

    payload = json.loads(endpoint_path.read_text(encoding="utf-8"))
    return EndpointInfo(
        base_url=str(payload["base_url"]),
        health_url=str(payload["health_url"]),
        model=str(payload["model"]),
        node=str(payload["node"]),
        port=int(payload["port"]),
        slurm_job_id=str(payload.get("slurm_job_id", "")),
        started_at=str(payload.get("started_at", "")),
        api_key_required=_coerce_bool(payload.get("api_key_required", False)),
    )


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes"}:
            return True
        if normalized in {"0", "false", "no"}:
            return False
    if isinstance(value, int):
        return bool(value)
    raise ValueError(f"Invalid boolean value: {value!r}")
