from __future__ import annotations

import contextlib
import os
from pathlib import Path
from typing import Any

from src.rag.service import RAGService


ROOT = Path(__file__).resolve().parents[2]
MACOS_GATEWAY = ROOT / "scripts" / "deployment" / "macos" / "run_rag_gateway.sh"
HPC_GATEWAY = ROOT / "scripts" / "deployment" / "hpc" / "run_rag_gateway.sbatch"
HPC_PHASE3 = ROOT / "scripts" / "deployment" / "hpc" / "run_phase3_openwebui_verification.sbatch"


class FakeDoc:
    def __init__(self, page_content: str, metadata: dict[str, Any] | None = None) -> None:
        self.page_content = page_content
        self.metadata = metadata or {}


class FakeRAGChain:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def invoke(self, prompt: str) -> dict[str, Any]:
        self.prompts.append(prompt)
        return {
            "answer": "Use sbatch.",
            "context": [
                FakeDoc(
                    "Submit Slurm jobs with sbatch.",
                    {"chunk_id": "chunk-1", "source": "slurm.md"},
                )
            ],
        }


class StreamingFakeRAGChain(FakeRAGChain):
    def stream_answer(self, prompt: str) -> dict[str, Any]:
        self.prompts.append(prompt)
        return {
            "chunks": ["Use ", "sbatch."],
            "context": [
                FakeDoc(
                    "Submit Slurm jobs with sbatch.",
                    {"chunk_id": "chunk-1", "source": "slurm.md"},
                )
            ],
        }


def test_rag_service_invokes_chain_and_logs_sanitized_telemetry(monkeypatch) -> None:
    chain = FakeRAGChain()
    jsonl_records: list[dict[str, Any]] = []
    params: dict[str, Any] = {}

    monkeypatch.setattr(
        "src.rag.service.mlflow_tracker.start_run",
        lambda **_: contextlib.nullcontext(),
    )
    monkeypatch.setattr(
        "src.rag.service.mlflow_tracker.log_jsonl",
        lambda records, _: jsonl_records.extend(records),
    )
    monkeypatch.setattr(
        "src.rag.service.mlflow_tracker.log_params",
        lambda payload: params.update(payload),
    )
    monkeypatch.setattr("src.rag.service.mlflow_tracker.log_metrics", lambda _: None)

    service = RAGService(chain_factory=lambda: chain)

    result = service.answer("How do I submit a Slurm job?")

    assert chain.prompts == ["How do I submit a Slurm job?"]
    assert result.answer == "Use sbatch."
    assert result.request_id.startswith("rag-")
    assert result.sources[0]["chunk_id"] == "chunk-1"
    assert result.metadata["prompt_hash"]
    assert result.metadata["retrieval_count"] == 1
    assert "How do I submit" not in str(jsonl_records)
    assert "Submit Slurm jobs" not in str(jsonl_records)
    assert jsonl_records[0]["query_id"] == result.request_id
    assert jsonl_records[0]["retrieved_doc_ids"] == ["chunk-1"]
    assert "_question" not in params


def test_rag_service_stream_finalization_records_completion_hash(monkeypatch) -> None:
    chain = StreamingFakeRAGChain()
    jsonl_records: list[dict[str, Any]] = []

    monkeypatch.setattr(
        "src.rag.service.mlflow_tracker.start_run",
        lambda **_: contextlib.nullcontext(),
    )
    monkeypatch.setattr(
        "src.rag.service.mlflow_tracker.log_jsonl",
        lambda records, _: jsonl_records.extend(records),
    )
    monkeypatch.setattr("src.rag.service.mlflow_tracker.log_params", lambda _: None)
    monkeypatch.setattr("src.rag.service.mlflow_tracker.log_metrics", lambda _: None)

    service = RAGService(chain_factory=lambda: chain)
    stream = service.start_stream("How do I submit a Slurm job?")
    answer = "".join(stream.chunks)
    metadata = service.finalize_stream(stream, answer)

    assert answer == "Use sbatch."
    assert metadata["completion_hash"]
    assert metadata["retrieval_count"] == 1
    assert jsonl_records[0]["request_id"] == stream.request_id
    assert "How do I submit" not in str(jsonl_records)


def test_rag_service_health_reports_degraded_provider_without_chain_init(monkeypatch) -> None:
    initialized = False

    def _factory():
        nonlocal initialized
        initialized = True
        return FakeRAGChain()

    def _fail_health(*_, **__):
        raise TimeoutError("provider unavailable")

    monkeypatch.setattr("src.rag.service.urlopen", _fail_health)

    payload = RAGService(chain_factory=_factory).health()

    assert initialized is False
    assert payload["status"] == "ok"
    assert payload["backend"]["provider_health"]["status"] == "degraded"
    assert payload["backend"]["provider_health"]["reason"] == "TimeoutError"


def test_rag_gateway_launch_scripts_exist_and_reference_fastapi_entrypoint() -> None:
    macos_text = MACOS_GATEWAY.read_text(encoding="utf-8")
    hpc_text = HPC_GATEWAY.read_text(encoding="utf-8")
    phase3_text = HPC_PHASE3.read_text(encoding="utf-8")

    assert os.access(MACOS_GATEWAY, os.X_OK)
    assert os.access(HPC_GATEWAY, os.X_OK)
    assert os.access(HPC_PHASE3, os.X_OK)
    assert "uvicorn src.rag.api:app" in macos_text
    assert "uvicorn src.rag.api:app" in hpc_text
    assert "uvicorn src.rag.api:app" in phase3_text
    assert "vllm serve" in phase3_text
    assert "oarc-rag-v1" in phase3_text
    assert "OpenWebUI" in phase3_text
    assert "RAG_GATEWAY_LLM_PROVIDER" in macos_text
    assert "RAG_GATEWAY_VECTOR_STORE" in hpc_text
