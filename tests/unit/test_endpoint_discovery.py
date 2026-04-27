from src.rag.endpoint_discovery import read_endpoint, resolve_endpoint_dir


def test_read_endpoint_returns_metadata(tmp_path) -> None:
    endpoint_dir = tmp_path / "shared" / "vllm"
    endpoint_dir.mkdir(parents=True)
    endpoint_file = endpoint_dir / "vllm-endpoint.json"
    endpoint_file.write_text(
        """
        {
          "base_url": "http://gpu-node:8000",
          "health_url": "http://gpu-node:8000/health",
          "model": "acme/model",
          "node": "gpu-node",
          "port": 8000,
          "slurm_job_id": "12345",
          "started_at": "2026-04-14T00:00:00Z",
          "api_key_required": true
        }
        """.strip(),
        encoding="utf-8",
    )

    endpoint = read_endpoint(endpoint_dir)

    assert endpoint is not None
    assert endpoint.base_url == "http://gpu-node:8000"
    assert endpoint.health_url == "http://gpu-node:8000/health"
    assert endpoint.model == "acme/model"
    assert endpoint.api_key_required is True


def test_resolve_endpoint_dir_uses_env(monkeypatch, tmp_path) -> None:
    endpoint_dir = tmp_path / "group" / "vllm-endpoints"
    monkeypatch.setenv("VLLM_ENDPOINT_DIR", str(endpoint_dir))

    assert resolve_endpoint_dir() == endpoint_dir


def test_read_endpoint_returns_none_when_missing(tmp_path) -> None:
    assert read_endpoint(tmp_path / "missing") is None
