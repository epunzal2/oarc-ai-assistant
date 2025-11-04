from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

"""Centralized configuration with env-first overrides.

These values provide convenient defaults for local runs while allowing Slurm
jobs and other environments to override via exported environment variables.
"""


def _env_int(name: str, default: Optional[int] = None) -> Optional[int]:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_float(name: str, default: Optional[float] = None) -> Optional[float]:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _json_env(name: str) -> Dict[str, Any]:
    raw = os.environ.get(name)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass
    return {}


@dataclass
class HTTPProviderSettings:
    """Configuration for HTTP-based (OpenAI-compatible) providers."""

    base_url: str
    model: str
    api_key: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    backoff_factor: float = 1.5
    system_prompt: Optional[str] = None
    tokenizer: Optional[str] = None
    max_context_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None
    health_port: Optional[int] = None
    request_kwargs: Dict[str, Any] = field(default_factory=dict)
    generation_kwargs: Dict[str, Any] = field(default_factory=dict)

    def to_provider_kwargs(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "base_url": self.base_url,
            "model": self.model,
            "api_key": self.api_key,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "backoff_factor": self.backoff_factor,
            "system_prompt": self.system_prompt,
            "tokenizer": self.tokenizer,
            "max_context_tokens": self.max_context_tokens,
            "max_output_tokens": self.max_output_tokens,
            "request_kwargs": self.request_kwargs or None,
        }
        payload.update(self.generation_kwargs)
        return {k: v for k, v in payload.items() if v is not None}

    def as_sanitized_dict(self) -> Dict[str, Any]:
        """Return a sanitized dict for logging/artifact purposes."""
        data = {
            "base_url": self.base_url,
            "model": self.model,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "backoff_factor": self.backoff_factor,
            "system_prompt_hash": (
                hash(self.system_prompt) if self.system_prompt else None
            ),
            "tokenizer": self.tokenizer,
            "max_context_tokens": self.max_context_tokens,
            "max_output_tokens": self.max_output_tokens,
            "health_port": self.health_port,
            "request_kwargs": self.request_kwargs,
            "generation_kwargs": self.generation_kwargs,
        }
        return data


def _load_http_provider(prefix: str, *, defaults: Dict[str, Any]) -> HTTPProviderSettings:
    base_url = os.environ.get(f"{prefix}_BASE_URL", defaults["base_url"])
    model = os.environ.get(f"{prefix}_MODEL", defaults["model"])
    api_key = os.environ.get(f"{prefix}_API_KEY")
    timeout = _env_float(f"{prefix}_TIMEOUT", defaults.get("timeout", 30.0)) or 30.0
    max_retries = _env_int(f"{prefix}_MAX_RETRIES", defaults.get("max_retries", 3)) or 3
    backoff_factor = _env_float(
        f"{prefix}_BACKOFF_FACTOR", defaults.get("backoff_factor", 1.5)
    ) or 1.5
    system_prompt = os.environ.get(f"{prefix}_SYSTEM_PROMPT", defaults.get("system_prompt"))
    tokenizer = os.environ.get(f"{prefix}_TOKENIZER", defaults.get("tokenizer"))
    max_context_tokens = _env_int(
        f"{prefix}_MAX_CONTEXT", defaults.get("max_context_tokens")
    )
    max_output_tokens = _env_int(
        f"{prefix}_MAX_OUTPUT_TOKENS", defaults.get("max_output_tokens")
    )
    health_port = _env_int(f"{prefix}_HEALTH_PORT", defaults.get("health_port"))
    request_kwargs = defaults.get("request_kwargs", {}).copy()
    request_kwargs.update(_json_env(f"{prefix}_REQUEST_KWARGS"))

    generation_kwargs = defaults.get("generation_kwargs", {}).copy()
    generation_kwargs.update(_json_env(f"{prefix}_GENERATION_JSON"))
    # Common scalar overrides
    for key in ("TEMPERATURE", "TOP_P", "TOP_K", "PRESENCE_PENALTY", "FREQUENCY_PENALTY", "MAX_TOKENS"):
        env_key = f"{prefix}_{key}"
        value = os.environ.get(env_key)
        if value is None:
            continue
        try:
            if key in {"TOP_K"}:
                generation_kwargs[key.lower()] = int(value)
            elif key in {"MAX_TOKENS"}:
                generation_kwargs["max_tokens"] = int(value)
            else:
                generation_kwargs[key.lower()] = float(value)
        except ValueError:
            continue

    return HTTPProviderSettings(
        base_url=base_url,
        model=model,
        api_key=api_key,
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
        system_prompt=system_prompt,
        tokenizer=tokenizer,
        max_context_tokens=max_context_tokens,
        max_output_tokens=max_output_tokens,
        health_port=health_port,
        request_kwargs=request_kwargs,
        generation_kwargs=generation_kwargs,
    )


# Path to the directory containing the markdown files
DATA_PATH = os.environ.get("DATA_PATH", "docs/google_sites_guide/")
SERVICE_NOW_DATA_PATH = os.environ.get(
    "SERVICE_NOW_DATA_PATH", "docs/servicenow/task_prepared.jsonl"
)

# Embedding model to use
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Qdrant configuration
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = os.environ.get("QDRANT_PORT", 6333)
QDRANT_COLLECTION_NAME = os.environ.get("QDRANT_COLLECTION_NAME", "rag_system_collection")

# Hugging Face API configuration
HF_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

# RAG and Llama.cpp server configuration
LLAMA_CPP_MODEL_PATH = os.environ.get(
    "LLAMA_CPP_MODEL_PATH", "models/Phi-3-mini-4k-instruct-q4.gguf"
)
FAISS_INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "vector_index/faiss_amarel")

DEFAULT_LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "llama_cpp").lower()

# HTTP providers (OpenAI-compatible)
VLLM_SETTINGS = _load_http_provider(
    "VLLM",
    defaults={
        "base_url": "http://127.0.0.1:8000",
        "model": "meta-llama/Llama-3-8B-Instruct",
        "timeout": 45.0,
        "max_retries": 5,
        "backoff_factor": 2.0,
        "max_context_tokens": 8192,
        "generation_kwargs": {"temperature": 0.0},
    },
)

SGLANG_SETTINGS = _load_http_provider(
    "SGLANG",
    defaults={
        "base_url": "http://127.0.0.1:30000",
        "model": "deepseek-ai/DeepSeek-V2.5",
        "timeout": 45.0,
        "max_retries": 5,
        "backoff_factor": 2.0,
        "max_context_tokens": 16384,
        "generation_kwargs": {"temperature": 0.1, "top_p": 0.95},
    },
)

HTTP_PROVIDER_CONFIGS: Dict[str, HTTPProviderSettings] = {
    "vllm": VLLM_SETTINGS,
    "vllm_api": VLLM_SETTINGS,
    "sglang": SGLANG_SETTINGS,
    "sglang_api": SGLANG_SETTINGS,
}


def provider_kwargs(provider_name: str) -> Dict[str, Any]:
    """Return kwargs for provider instantiation using config settings."""
    normalized = provider_name.lower()
    settings = HTTP_PROVIDER_CONFIGS.get(normalized)
    if settings:
        return settings.to_provider_kwargs()
    # For non-HTTP providers we fall back to env-supplied kwargs (currently none)
    return {}


def provider_health_port(provider_name: str) -> Optional[int]:
    settings = HTTP_PROVIDER_CONFIGS.get(provider_name.lower())
    return settings.health_port if settings else None


def persist_provider_settings(provider_name: str, directory: Path) -> Optional[Path]:
    """Persist sanitized provider settings for observability (optional)."""
    directory.mkdir(parents=True, exist_ok=True)
    settings = HTTP_PROVIDER_CONFIGS.get(provider_name.lower())
    if not settings:
        return None
    path = directory / f"{provider_name.lower()}_config.json"
    with path.open("w") as handle:
        json.dump(settings.as_sanitized_dict(), handle, indent=2)
    return path


@dataclass(frozen=True)
class MLflowSettings:
    """Configuration block for MLflow integration."""

    enabled: bool = field(default_factory=lambda: _env_bool("MLFLOW_ENABLED", True))
    tracking_uri: str = field(
        default_factory=lambda: os.environ.get("MLFLOW_TRACKING_URI", "file:mlruns")
    )
    experiment_name: str = field(
        default_factory=lambda: os.environ.get("MLFLOW_EXPERIMENT_NAME", "rag-evals")
    )
    runtime_sampling_probability: float = field(
        default_factory=lambda: _env_float("MLFLOW_RUNTIME_SAMPLE_P", 0.1) or 0.1
    )
    artifact_top_k: int = field(
        default_factory=lambda: _env_int("MLFLOW_ARTIFACT_TOP_K", 5) or 5
    )
    artifact_max_bytes: int = field(
        default_factory=lambda: _env_int("MLFLOW_ARTIFACT_MAX_BYTES", 65_536) or 65_536
    )
    sampler_timeout_seconds: float = field(
        default_factory=lambda: _env_float("MLFLOW_SAMPLER_TIMEOUT_S", 2.5) or 2.5
    )
    sampler_backoff_seconds: float = field(
        default_factory=lambda: _env_float("MLFLOW_SAMPLER_BACKOFF_S", 60.0) or 60.0
    )

    def as_tags(self) -> Dict[str, Any]:
        """Lightweight dict for tagging/testing."""
        return {
            "tracking_uri": self.tracking_uri,
            "experiment_name": self.experiment_name,
            "artifact_top_k": self.artifact_top_k,
        }


@dataclass(frozen=True)
class TelemetrySettings:
    """Background telemetry sampler controls."""

    enabled: bool = field(default_factory=lambda: _env_bool("TELEMETRY_ENABLED", True))
    interval_seconds: float = field(
        default_factory=lambda: _env_float("TELEMETRY_INTERVAL_S", 30.0) or 30.0
    )
    sample_window: int = field(default_factory=lambda: _env_int("TELEMETRY_WINDOW", 5) or 5)
    record_gpu: bool = field(default_factory=lambda: _env_bool("TELEMETRY_GPU_ENABLED", True))
    fail_silently: bool = field(
        default_factory=lambda: _env_bool("TELEMETRY_FAIL_SILENTLY", True)
    )


MLFLOW = MLflowSettings()
TELEMETRY = TelemetrySettings()
