from importlib import reload
from unittest.mock import MagicMock, patch

from src.rag import config as config_module
from src.rag.llm_provider import VLLMProvider


def test_vllm_provider_non_streaming(monkeypatch):
    provider = VLLMProvider(
        base_url="http://localhost:8000",
        model="test-model",
        max_context_tokens=8192,
        max_output_tokens=64,
    )

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "hello world"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
    }

    with patch("src.rag.llm_provider.requests.post", return_value=mock_response):
        result = provider.generate("hi there", stream=False)

    assert result.text == "hello world"
    assert result.usage.prompt_tokens == 10
    assert result.usage.completion_tokens == 2
    assert result.usage.total_tokens == 12
    mock_response.close.assert_called_once()


def test_vllm_provider_streaming(monkeypatch):
    provider = VLLMProvider(
        base_url="http://localhost:8000",
        model="test-model",
        max_context_tokens=2048,
        max_output_tokens=32,
    )

    chunks = [
        'data: {"choices": [{"delta": {"content": "Hello"}}]}',
        'data: {"choices": [{"delta": {"content": "!"}}], "usage": {"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7}}',
        "data: [DONE]",
    ]

    def _iter_lines(*_, **__):
        for item in chunks:
            yield item

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.side_effect = _iter_lines

    with patch("src.rag.llm_provider.requests.post", return_value=mock_response):
        result = provider.generate("hello?", stream=True)
        tokens = list(result.stream or [])

    assert tokens == ["Hello", "!"]
    assert result.usage.prompt_tokens is not None
    assert result.usage.completion_tokens >= 2
    assert result.usage.total_tokens == result.usage.prompt_tokens + result.usage.completion_tokens
    mock_response.close.assert_called_once()


def test_config_provider_kwargs(monkeypatch):
    monkeypatch.setenv("VLLM_BASE_URL", "http://gpu-node:9000")
    monkeypatch.setenv("VLLM_MODEL", "acme/my-model")
    monkeypatch.setenv("VLLM_TIMEOUT", "12")
    monkeypatch.setenv("VLLM_MAX_RETRIES", "9")
    monkeypatch.setenv("VLLM_BACKOFF_FACTOR", "3.5")
    monkeypatch.setenv("VLLM_HEALTH_PORT", "6100")
    monkeypatch.setenv("VLLM_TEMPERATURE", "0.25")

    reload(config_module)

    kwargs = config_module.provider_kwargs("vllm")
    assert kwargs["base_url"] == "http://gpu-node:9000"
    assert kwargs["model"] == "acme/my-model"
    assert kwargs["timeout"] == 12.0
    assert kwargs["max_retries"] == 9
    assert kwargs["backoff_factor"] == 3.5
    assert kwargs["temperature"] == 0.25
    assert config_module.provider_health_port("vllm") == 6100

    # Cleanup to avoid side effects on subsequent imports
    for key in (
        "VLLM_BASE_URL",
        "VLLM_MODEL",
        "VLLM_TIMEOUT",
        "VLLM_MAX_RETRIES",
        "VLLM_BACKOFF_FACTOR",
        "VLLM_HEALTH_PORT",
        "VLLM_TEMPERATURE",
    ):
        monkeypatch.delenv(key, raising=False)
    reload(config_module)
