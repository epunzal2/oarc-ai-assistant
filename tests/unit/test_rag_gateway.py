from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from src.rag.api import RAG_MODEL_ID, create_app


class FakeDoc:
    def __init__(self, page_content: str, metadata: dict | None = None) -> None:
        self.page_content = page_content
        self.metadata = metadata or {}


class FakeRAGChain:
    def __init__(self, result="RAG answer") -> None:
        self.result = result
        self.prompts: list[str] = []

    def invoke(self, prompt: str):
        self.prompts.append(prompt)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class StreamingFakeRAGChain(FakeRAGChain):
    def __init__(self, chunks, context=None) -> None:
        super().__init__()
        self.chunks = chunks
        self.context = context or []

    def stream_answer(self, prompt: str):
        self.prompts.append(prompt)
        return {"chunks": self.chunks, "context": self.context}


def _client_for(chain: FakeRAGChain) -> TestClient:
    return TestClient(create_app(rag_chain_factory=lambda: chain))


def _sse_payloads(text: str) -> list[dict]:
    payloads = []
    for block in text.strip().split("\n\n"):
        for line in block.splitlines():
            if line.startswith("data: ") and line != "data: [DONE]":
                payloads.append(json.loads(line.removeprefix("data: ")))
    return payloads


def test_health_returns_stable_shape_without_initializing_rag_chain() -> None:
    initialized = False

    def _factory():
        nonlocal initialized
        initialized = True
        return FakeRAGChain()

    client = TestClient(create_app(rag_chain_factory=_factory))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "rag-gateway"
    assert response.json()["model"] == RAG_MODEL_ID
    assert "backend" in response.json()
    assert initialized is False


def test_models_returns_openai_style_model_list() -> None:
    client = _client_for(FakeRAGChain())

    response = client.get("/v1/models")

    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "list"
    assert payload["data"][0]["id"] == RAG_MODEL_ID
    assert payload["data"][0]["object"] == "model"
    assert payload["data"][0]["metadata"]["rag"] is True
    assert payload["data"][0]["metadata"]["backing_provider"] == "vllm"


def test_chat_completion_extracts_latest_user_message_and_returns_response_shape() -> None:
    docs = [
        FakeDoc(
            "Submit batch jobs with sbatch.",
            {"chunk_id": "chunk-1", "source": "slurm.md", "title": "Slurm"},
        )
    ]
    chain = FakeRAGChain({"answer": "Use sbatch to submit jobs.", "context": docs})
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "messages": [
                {"role": "system", "content": "Be concise."},
                {"role": "user", "content": "How do I allocate a GPU?"},
                {"role": "assistant", "content": "Previous answer."},
                {"role": "user", "content": "How do I submit a batch job?"},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert chain.prompts == ["How do I submit a batch job?"]
    assert payload["id"].startswith("chatcmpl-")
    assert payload["object"] == "chat.completion"
    assert isinstance(payload["created"], int)
    assert payload["model"] == RAG_MODEL_ID
    assert payload["rag_request_id"].startswith("rag-")
    assert payload["rag_sources"] == [
        {
            "source": "slurm.md",
            "title": "Slurm",
            "chunk_id": "chunk-1",
            "snippet": "Submit batch jobs with sbatch.",
        }
    ]
    assert payload["choices"] == [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Use sbatch to submit jobs.",
            },
            "finish_reason": "stop",
        }
    ]
    assert payload["usage"]["prompt_tokens"] > 0
    assert payload["usage"]["completion_tokens"] > 0
    assert payload["usage"]["total_tokens"] == (
        payload["usage"]["prompt_tokens"] + payload["usage"]["completion_tokens"]
    )


def test_chat_completion_normalizes_dict_answer() -> None:
    chain = FakeRAGChain({"answer": "Dictionary answer"})
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "messages": [{"role": "user", "content": "What is Amarel?"}],
        },
    )

    assert response.status_code == 200
    assert response.json()["choices"][0]["message"]["content"] == "Dictionary answer"
    assert response.json()["rag_sources"] == []


def test_chat_completion_supports_simple_text_content_parts() -> None:
    chain = FakeRAGChain("Answer")
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Line one."},
                        {"type": "image_url", "image_url": {"url": "ignored"}},
                        {"type": "text", "text": "Line two."},
                    ],
                }
            ],
        },
    )

    assert response.status_code == 200
    assert chain.prompts == ["Line one.\nLine two."]


def test_chat_completion_streams_openai_chunks_and_sources() -> None:
    docs = [
        FakeDoc(
            "GPU jobs need a GPU partition and GRES request.",
            {
                "id": "doc-1",
                "chunk_id": "chunk-1",
                "source": "gpu.md",
                "url": "https://example.edu/gpu",
                "score": 0.91,
            },
        )
    ]
    chain = StreamingFakeRAGChain(["Use ", "salloc."], context=docs)
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "stream": True,
            "messages": [{"role": "user", "content": "How do I get a GPU?"}],
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert chain.prompts == ["How do I get a GPU?"]
    assert "data: [DONE]" in response.text
    payloads = _sse_payloads(response.text)
    assert payloads[0]["choices"][0]["delta"] == {"role": "assistant"}
    assert payloads[1]["choices"][0]["delta"] == {"content": "Use "}
    assert payloads[2]["choices"][0]["delta"] == {"content": "salloc."}
    assert payloads[-1]["choices"][0]["finish_reason"] == "stop"
    assert payloads[-1]["rag_request_id"].startswith("rag-")
    assert payloads[-1]["rag_sources"] == [
        {
            "id": "doc-1",
            "source": "gpu.md",
            "url": "https://example.edu/gpu",
            "chunk_id": "chunk-1",
            "score": 0.91,
            "snippet": "GPU jobs need a GPU partition and GRES request.",
        }
    ]


def test_chat_completion_streaming_falls_back_to_single_content_chunk() -> None:
    chain = FakeRAGChain("Fallback answer")
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "stream": True,
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )

    assert response.status_code == 200
    payloads = _sse_payloads(response.text)
    assert payloads[1]["choices"][0]["delta"] == {"content": "Fallback answer"}
    assert payloads[-1]["choices"][0]["finish_reason"] == "stop"


def test_chat_completion_streaming_setup_error_returns_json() -> None:
    chain = FakeRAGChain(RuntimeError("retrieval failed"))
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "stream": True,
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )

    assert response.status_code == 500
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["error"]["type"] == "server_error"


def test_chat_completion_streaming_midstream_error_emits_error_event() -> None:
    def _chunks():
        yield "partial"
        raise RuntimeError("provider exploded")

    chain = StreamingFakeRAGChain(_chunks())
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "stream": True,
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )

    assert response.status_code == 200
    assert 'event: error\ndata: {"error":{"message":"The RAG gateway failed while streaming' in response.text
    assert "provider exploded" not in response.text
    assert response.text.endswith("data: [DONE]\n\n")


def test_source_extraction_omits_missing_metadata_and_deduplicates() -> None:
    repeated = FakeDoc("Same chunk", {"chunk_id": "same", "source": "a.md"})
    chain = FakeRAGChain(
        {
            "answer": "Answer",
            "context": [
                repeated,
                FakeDoc("Same chunk duplicate", {"chunk_id": "same", "source": "a.md"}),
                FakeDoc("Only content"),
            ],
        }
    )
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )

    assert response.status_code == 200
    assert response.json()["rag_sources"] == [
        {"source": "a.md", "chunk_id": "same", "snippet": "Same chunk"},
        {"snippet": "Only content"},
    ]


def test_chat_completion_requires_non_empty_user_message() -> None:
    client = _client_for(FakeRAGChain())

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "messages": [
                {"role": "system", "content": "Help."},
                {"role": "user", "content": "   "},
            ],
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["type"] == "invalid_request_error"
    assert "non-empty user message" in response.json()["error"]["message"]


def test_chat_completion_requires_messages() -> None:
    client = _client_for(FakeRAGChain())

    response = client.post(
        "/v1/chat/completions",
        json={"model": RAG_MODEL_ID, "messages": []},
    )

    assert response.status_code == 422
    assert response.json()["error"]["type"] == "invalid_request_error"


def test_chat_completion_returns_openai_style_server_error() -> None:
    client = _client_for(FakeRAGChain(RuntimeError("backend stack details")))

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )

    assert response.status_code == 500
    payload = response.json()
    assert payload["error"]["type"] == "server_error"
    assert "backend stack details" not in payload["error"]["message"]


def test_design_marks_phase_1_complete() -> None:
    design = Path("project_docs/DESIGN.md").read_text(encoding="utf-8")
    phase_1 = design.split("### Phase 1: RAG-Compatible API Boundary", 1)[1].split(
        "### Phase 2:", 1
    )[0]

    assert "- [ ]" not in phase_1
    assert ".plans/2026-04-27-rag-openai-api-boundary.md" in phase_1
    assert "src/rag/api.py" in phase_1
    assert "tests/unit/test_rag_gateway.py" in phase_1
