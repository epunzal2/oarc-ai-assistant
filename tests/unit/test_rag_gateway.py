from __future__ import annotations

from fastapi.testclient import TestClient

from src.rag.api import RAG_MODEL_ID, create_app


class FakeRAGChain:
    def __init__(self, result="RAG answer") -> None:
        self.result = result
        self.prompts: list[str] = []

    def invoke(self, prompt: str):
        self.prompts.append(prompt)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def _client_for(chain: FakeRAGChain) -> TestClient:
    return TestClient(create_app(rag_chain_factory=lambda: chain))


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
    chain = FakeRAGChain("Use sbatch to submit jobs.")
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


def test_chat_completion_rejects_streaming() -> None:
    chain = FakeRAGChain()
    client = _client_for(chain)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": RAG_MODEL_ID,
            "stream": True,
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "streaming_unsupported"
    assert chain.prompts == []


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
