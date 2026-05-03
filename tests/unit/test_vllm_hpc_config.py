"""Configuration precedence tests for vLLM/SGLang HPC providers."""

from importlib import reload

from src.rag import config as config_module


def test_vllm_endpoint_dir_supplies_provider_defaults(monkeypatch, tmp_path) -> None:
    endpoint_dir = tmp_path / "shared" / "vllm"
    endpoint_dir.mkdir(parents=True)
    (endpoint_dir / "vllm-endpoint.json").write_text(
        """
        {
          "base_url": "http://gpu-node:8100",
          "health_url": "http://gpu-node:8100/health",
          "model": "acme/served-model",
          "node": "gpu-node",
          "port": 8100,
          "slurm_job_id": "98765",
          "started_at": "2026-04-14T00:00:00Z",
          "api_key_required": false
        }
        """.strip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("VLLM_ENDPOINT_DIR", str(endpoint_dir))
    for key in ("VLLM_BASE_URL", "VLLM_MODEL", "VLLM_HEALTH_URL"):
        monkeypatch.delenv(key, raising=False)

    reload(config_module)

    kwargs = config_module.provider_kwargs("vllm")
    assert kwargs["base_url"] == "http://gpu-node:8100"
    assert kwargs["model"] == "acme/served-model"
    assert config_module.provider_health_url("vllm") == "http://gpu-node:8100/health"

    monkeypatch.delenv("VLLM_ENDPOINT_DIR", raising=False)
    reload(config_module)


def test_explicit_vllm_env_overrides_endpoint_file(monkeypatch, tmp_path) -> None:
    endpoint_dir = tmp_path / "shared" / "vllm"
    endpoint_dir.mkdir(parents=True)
    (endpoint_dir / "vllm-endpoint.json").write_text(
        """
        {
          "base_url": "http://gpu-node:8100",
          "health_url": "http://gpu-node:8100/health",
          "model": "acme/served-model",
          "node": "gpu-node",
          "port": 8100,
          "slurm_job_id": "98765",
          "started_at": "2026-04-14T00:00:00Z",
          "api_key_required": false
        }
        """.strip(),
        encoding="utf-8",
    )
    monkeypatch.setenv("VLLM_ENDPOINT_DIR", str(endpoint_dir))
    monkeypatch.setenv("VLLM_BASE_URL", "http://override:9000")
    monkeypatch.setenv("VLLM_MODEL", "override-model")
    monkeypatch.setenv("VLLM_HEALTH_URL", "http://override:9000/ready")

    reload(config_module)

    kwargs = config_module.provider_kwargs("vllm")
    assert kwargs["base_url"] == "http://override:9000"
    assert kwargs["model"] == "override-model"
    assert config_module.provider_health_url("vllm") == "http://override:9000/ready"

    for key in ("VLLM_ENDPOINT_DIR", "VLLM_BASE_URL", "VLLM_MODEL", "VLLM_HEALTH_URL"):
        monkeypatch.delenv(key, raising=False)
    reload(config_module)


def test_sglang_health_url_falls_back_to_health_port(monkeypatch) -> None:
    monkeypatch.setenv("SGLANG_BASE_URL", "http://sglang-node:30000")
    monkeypatch.setenv("SGLANG_HEALTH_PORT", "30001")

    reload(config_module)

    assert (
        config_module.provider_health_url("sglang", host="127.0.0.1")
        == "http://127.0.0.1:30001/healthz"
    )

    for key in ("SGLANG_BASE_URL", "SGLANG_HEALTH_PORT"):
        monkeypatch.delenv(key, raising=False)
    reload(config_module)
