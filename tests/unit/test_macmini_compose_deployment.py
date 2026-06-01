"""Contract tests for the Mac mini Docker Compose deployment path."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "compose.macmini.yaml"
DOCKERIGNORE = ROOT / ".dockerignore"
DOCKERFILE = ROOT / "Dockerfile"
MACMINI_SCRIPTS = ROOT / "scripts" / "deployment" / "macmini"


def test_macmini_compose_wires_gateway_to_ollama_and_faiss() -> None:
    content = COMPOSE.read_text(encoding="utf-8")

    assert "127.0.0.1:${RAG_GATEWAY_PORT:-8088}:8088" in content
    assert "RAG_GATEWAY_LLM_PROVIDER: ${RAG_GATEWAY_LLM_PROVIDER:-vllm}" in content
    assert "RAG_GATEWAY_VECTOR_STORE: ${RAG_GATEWAY_VECTOR_STORE:-faiss}" in content
    assert "RAG_RETRIEVAL_MODE: ${RAG_RETRIEVAL_MODE:-vector}" in content
    assert "RAG_VECTOR_TOP_K: ${RAG_VECTOR_TOP_K:-20}" in content
    assert "RAG_KEYWORD_TOP_K: ${RAG_KEYWORD_TOP_K:-20}" in content
    assert "RAG_RERANK_TOP_K: ${RAG_RERANK_TOP_K:-8}" in content
    assert "RAG_FINAL_TOP_K: ${RAG_FINAL_TOP_K:-4}" in content
    assert "RAG_RERANKER_ENABLED: ${RAG_RERANKER_ENABLED:-false}" in content
    assert "RAG_RERANKER_REQUIRED: ${RAG_RERANKER_REQUIRED:-false}" in content
    assert "VLLM_BASE_URL: ${VLLM_BASE_URL:-http://host.docker.internal:11434}" in content
    assert "VLLM_MODEL: ${VLLM_MODEL:-llama3.2:1b}" in content
    assert (
        "VLLM_HEALTH_URL: ${VLLM_HEALTH_URL:-http://host.docker.internal:11434/v1/models}"
        in content
    )
    assert "FAISS_INDEX_PATH: ${FAISS_INDEX_PATH:-vector_index/faiss_macmini}" in content
    assert "EMBEDDING_MODEL: ${EMBEDDING_MODEL:-sentence-transformers/all-MiniLM-L6-v2}" in content
    assert "RAG_UI_ATTACHMENTS_ENABLED: ${RAG_UI_ATTACHMENTS_ENABLED:-true}" in content
    assert "curl -fsS http://127.0.0.1:8088/health" in content


def test_macmini_indexer_requires_prepared_servicenow_jsonl() -> None:
    content = COMPOSE.read_text(encoding="utf-8")

    assert (
        "SERVICE_NOW_DATA_PATH: ${SERVICE_NOW_DATA_PATH:-docs/servicenow/task_prepared.jsonl}"
        in content
    )
    assert "profiles: [\"index\"]" in content
    assert "test -f \"$${SERVICE_NOW_DATA_PATH}\"" in content
    assert "--servicenow-path \"$${SERVICE_NOW_DATA_PATH}\"" in content
    assert "--persist-dir \"$${FAISS_INDEX_PATH}\"" in content


def test_docker_context_excludes_raw_servicenow_and_runtime_state() -> None:
    content = DOCKERIGNORE.read_text(encoding="utf-8")

    for blocked in (
        ".env",
        "models/",
        "vector_index/",
        "runtime/",
        "logs/",
        "mlruns/",
        "docs/servicenow/task*.json",
    ):
        assert blocked in content
    assert "!docs/servicenow/task_prepared.jsonl" in content


def test_dockerfile_uses_base_dependencies_without_llm_runtime_extras() -> None:
    content = DOCKERFILE.read_text(encoding="utf-8")

    assert "FROM python:3.11-slim" in content
    assert "uv sync --python /usr/local/bin/python3 --frozen --no-dev" in content
    assert "UV_PYTHON_DOWNLOADS=never" in content
    assert "libmagic1" in content
    assert "--extra vllm" not in content
    assert "--extra sglang" not in content
    assert "--extra llama_cpp" not in content


def test_macmini_deploy_preserves_server_owned_state() -> None:
    content = (MACMINI_SCRIPTS / "deploy.sh").read_text(encoding="utf-8")

    assert "rsync -azc --whole-file --delete" in content

    for protected in (
        "--filter='P .env'",
        "--filter='P runtime/***'",
        "--filter='P vector_index/***'",
        "--filter='P logs/***'",
        "--filter='P mlruns/***'",
    ):
        assert protected in content

    for excluded in (
        "--exclude \".env\"",
        "--exclude \"models/\"",
        "--exclude \"docs/servicenow/task*.json\"",
    ):
        assert excluded in content


def test_macmini_scripts_are_executable_and_check_ollama() -> None:
    expected_scripts = [
        "deploy.sh",
        "logs.sh",
        "preflight.sh",
        "index.sh",
        "health.sh",
        "smoke.sh",
        "ui.sh",
    ]

    for script in expected_scripts:
        path = MACMINI_SCRIPTS / script
        assert path.exists()
        assert os.access(path, os.X_OK)

    preflight = (MACMINI_SCRIPTS / "preflight.sh").read_text(encoding="utf-8")
    assert "/opt/homebrew/bin/brew install ollama" in preflight
    assert "/opt/homebrew/bin/brew services start ollama" in preflight
    assert "ollama pull ${OLLAMA_MODEL}" in preflight
    assert "${OLLAMA_BASE_URL}/v1/models" in preflight


def test_macmini_ui_tunnel_script_targets_gateway_hosted_ui() -> None:
    script = MACMINI_SCRIPTS / "ui.sh"
    content = script.read_text(encoding="utf-8")

    assert os.access(script, os.X_OK)
    assert "LOCAL_UI_PORT=\"${LOCAL_UI_PORT:-18088}\"" in content
    assert "RAG UI: http://127.0.0.1:${LOCAL_UI_PORT}/ui" in content
    assert "127.0.0.1:${LOCAL_UI_PORT}:127.0.0.1:${RAG_GATEWAY_PORT}" in content
    assert "--print" in content
    assert "curl -fsS http://127.0.0.1:${RAG_GATEWAY_PORT}/health" in content
