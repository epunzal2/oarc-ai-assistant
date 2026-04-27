from __future__ import annotations

import hashlib
import json
import math
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, Optional

import requests

from src.rag.config import HF_API_TOKEN, LLAMA_CPP_MODEL_PATH
from src.rag.logger import get_logger

try:  # Optional dependency; used when available for accurate counts
    import tiktoken  # type: ignore
except Exception:  # pragma: no cover - best effort fallback
    tiktoken = None

logger = get_logger(__name__)


@dataclass
class LLMUsage:
    """Tracks prompt/completion token usage for observability."""

    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


@dataclass
class LLMResponse:
    """Container returned by provider.generate."""

    text: Optional[str] = None
    usage: LLMUsage = field(default_factory=LLMUsage)
    stream: Optional[Iterable[str]] = None
    raw: Any = None


def tokenize_len(text: str, *, encoding: Optional[str] = None) -> int:
    """Best-effort token count used for context guards and usage stats."""
    text = _prompt_to_text(text)
    if not text:
        return 0

    if tiktoken is not None:
        enc_name = encoding or "cl100k_base"
        try:
            encoder = tiktoken.get_encoding(enc_name)
        except Exception:  # pragma: no cover - unknown encoding
            encoder = tiktoken.get_encoding("cl100k_base")
        try:
            return len(encoder.encode(text))
        except Exception:  # pragma: no cover - fallback below
            pass

    # Fallback: rough heuristic (4 chars ~= 1 token)
    return max(1, math.ceil(len(text) / 4))


def _hash_prompt(prompt: str) -> str:
    prompt = _prompt_to_text(prompt)
    return hashlib.sha256(prompt.encode("utf-8", errors="ignore")).hexdigest()


def _prompt_to_text(prompt: Any) -> str:
    if isinstance(prompt, str):
        return prompt
    to_string = getattr(prompt, "to_string", None)
    if callable(to_string):
        return str(to_string())
    return str(prompt)


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    def __init__(
        self,
        *,
        max_context_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        tokenizer: Optional[str] = None,
    ) -> None:
        self.max_context_tokens = max_context_tokens
        self.max_output_tokens = max_output_tokens
        self._tokenizer = tokenizer

    @abstractmethod
    def get_llm(self):
        """Return a LangChain-compatible runnable."""

    def supports_streaming(self) -> bool:
        return False

    def _guard_prompt(self, prompt: str) -> int:
        prompt = _prompt_to_text(prompt)
        prompt_tokens = tokenize_len(prompt, encoding=self._tokenizer)
        if (
            self.max_context_tokens
            and self.max_output_tokens
            and prompt_tokens + self.max_output_tokens > self.max_context_tokens
        ):
            raise ValueError(
                f"Prompt ({prompt_tokens} tokens) + requested output "
                f"({self.max_output_tokens}) exceeds context window "
                f"({self.max_context_tokens}). Reduce context or max tokens."
            )
        return prompt_tokens

    @abstractmethod
    def generate(self, prompt: str, *, stream: bool = False) -> LLMResponse:
        """Execute a completion call."""

    def _normalize_text(self, response: Any) -> str:
        if isinstance(response, str):
            return response
        content = getattr(response, "content", None)
        if content is not None:
            return content
        return str(response)

    def get_completion(
        self,
        prompt: str,
        *,
        stream: bool = False,
        return_metadata: bool = False,
    ):
        if stream and not self.supports_streaming():
            raise NotImplementedError(
                f"{self.__class__.__name__} does not support streaming completions."
            )
        prompt_hash = _hash_prompt(prompt)
        logger.debug(
            "Dispatching completion via %s (prompt_hash=%s, stream=%s)",
            self.__class__.__name__,
            prompt_hash,
            stream,
        )
        result = self.generate(prompt, stream=stream)
        if return_metadata:
            return result
        if stream:
            return result.stream
        return result.text or ""


class HuggingFaceAPIProvider(LLMProvider):
    """
    LLM provider for the Hugging Face API.
    """

    def __init__(
        self,
        api_token: Optional[str] = HF_API_TOKEN,
        model_name: Optional[str] = None,
        *,
        max_context_tokens: Optional[int] = None,
        tokenizer: Optional[str] = None,
        **generation_kwargs,
    ):
        if not api_token:
            raise ValueError("Hugging Face API token is required.")
        self.api_token = api_token
        self.model_name = (
            model_name
            or os.environ.get("HF_MODEL_NAME")
            or os.environ.get("HUGGINGFACE_MODEL_NAME")
        )
        if not self.model_name:
            raise ValueError(
                "Hugging Face model name is required. Provide 'model_name' or set HF_MODEL_NAME."
            )

        defaults: Dict[str, Any] = {
            "temperature": 0.1,
            "max_new_tokens": 512,
        }
        defaults.update(generation_kwargs)
        super().__init__(
            max_context_tokens=max_context_tokens,
            max_output_tokens=defaults.get("max_new_tokens"),
            tokenizer=tokenizer,
        )
        self.generation_kwargs = defaults
        self._cached_llm = None
        logger.info(
            "Initialized HuggingFaceAPIProvider with model: %s (args hashed=%s)",
            self.model_name,
            _hash_prompt(json.dumps(self.generation_kwargs, sort_keys=True)),
        )

    def _get_or_create_llm(self):
        if self._cached_llm is None:
            logger.info("Creating Hugging Face LLM endpoint.")
            from langchain_huggingface import HuggingFaceEndpoint
            from langchain_huggingface.chat_models import ChatHuggingFace

            endpoint = HuggingFaceEndpoint(
                repo_id=self.model_name,
                huggingfacehub_api_token=self.api_token,
                **self.generation_kwargs,
            )
            self._cached_llm = ChatHuggingFace(llm=endpoint)
        return self._cached_llm

    def get_llm(self):
        return self._get_or_create_llm()

    def generate(self, prompt: str, *, stream: bool = False) -> LLMResponse:
        if stream:
            raise NotImplementedError("HuggingFaceEndpoint streaming unsupported in this runtime.")
        prompt_tokens = self._guard_prompt(prompt)
        llm = self._get_or_create_llm()
        response = llm.invoke(prompt)
        text = self._normalize_text(response)
        completion_tokens = tokenize_len(text, encoding=self._tokenizer)
        usage = LLMUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=(
                (prompt_tokens or 0) + (completion_tokens or 0)
                if prompt_tokens or completion_tokens
                else None
            ),
        )
        return LLMResponse(text=text, usage=usage, raw=response)


class LlamaCPPProvider(LLMProvider):
    """
    LLM provider for a local Llama.cpp model.
    """

    def __init__(
        self,
        model_path: str = LLAMA_CPP_MODEL_PATH,
        *,
        chat_format: Optional[str] = None,
        chat_template: Optional[str] = None,
        tokenizer: Optional[str] = None,
        max_context_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        **model_kwargs,
    ):
        defaults: Dict[str, Any] = {
            "n_gpu_layers": -1,
            "n_batch": 512,
            "n_ctx": 4096,
            "f16_kv": True,
            "verbose": True,
        }
        defaults.update(model_kwargs)
        if chat_format:
            defaults["chat_format"] = chat_format
        if chat_template:
            defaults["chat_template"] = chat_template

        super().__init__(
            max_context_tokens=max_context_tokens or defaults.get("n_ctx"),
            max_output_tokens=max_output_tokens or defaults.get("max_tokens") or defaults.get("max_new_tokens"),
            tokenizer=tokenizer,
        )
        self.model_path = model_path
        self.model_kwargs = defaults
        self._cached_llm: Optional[Any] = None
        logger.info("Initialized LlamaCPPProvider with model: %s", self.model_path)

    def _get_or_create_llm(self) -> Any:
        if self._cached_llm is None:
            logger.info("Creating Llama.cpp LLM instance.")
            from langchain_community.llms import LlamaCpp

            self._cached_llm = LlamaCpp(
                model_path=self.model_path,
                **self.model_kwargs,
            )
        return self._cached_llm

    def get_llm(self):
        return self._get_or_create_llm()

    def generate(self, prompt: str, *, stream: bool = False) -> LLMResponse:
        if stream:
            raise NotImplementedError("LlamaCpp streaming is not wired into the pipeline yet.")
        prompt_tokens = self._guard_prompt(prompt)
        llm = self._get_or_create_llm()
        response = llm.invoke(prompt)
        text = self._normalize_text(response)
        completion_tokens = tokenize_len(text, encoding=self._tokenizer)
        usage = LLMUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=(
                (prompt_tokens or 0) + (completion_tokens or 0)
                if prompt_tokens or completion_tokens
                else None
            ),
        )
        return LLMResponse(text=text, usage=usage, raw=response)


class OpenAICompatibleHTTPProvider(LLMProvider):
    """Base provider for OpenAI-compatible chat completion servers."""

    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        api_key: Optional[str] = None,
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
        system_prompt: Optional[str] = None,
        tokenizer: Optional[str] = None,
        max_context_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        request_kwargs: Optional[Dict[str, Any]] = None,
        **generation_kwargs,
    ):
        super().__init__(
            max_context_tokens=max_context_tokens,
            max_output_tokens=max_output_tokens or generation_kwargs.get("max_tokens"),
            tokenizer=tokenizer,
        )
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.system_prompt = system_prompt
        self.request_kwargs = request_kwargs or {}
        self.generation_kwargs = generation_kwargs
        self.default_headers = default_headers or {}
        self._completions_url = f"{self.base_url}/v1/chat/completions"
        logger.info(
            "Initialized %s targeting %s (model=%s, params_hash=%s)",
            self.__class__.__name__,
            self._completions_url,
            self.model,
            _hash_prompt(json.dumps(generation_kwargs, sort_keys=True)),
        )

    def supports_streaming(self) -> bool:
        return True

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        headers.update(self.default_headers)
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _payload(self, prompt: str, *, stream: bool) -> Dict[str, Any]:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }
        payload.update(self.generation_kwargs)
        if self.max_output_tokens and "max_tokens" not in payload:
            payload["max_tokens"] = self.max_output_tokens
        return payload

    def _post(self, payload: Dict[str, Any], *, stream: bool):
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    self._completions_url,
                    headers=self._headers(),
                    json=payload,
                    timeout=self.timeout,
                    stream=stream,
                    **self.request_kwargs,
                )
                if response.status_code >= 400:
                    detail = response.text[:500]
                    raise ValueError(
                        f"HTTP {response.status_code} during completion request: {detail}"
                    )
                return response
            except Exception as exc:
                last_exc = exc
                wait_time = self.backoff_factor ** (attempt - 1)
                logger.warning(
                    "%s request failed (attempt %s/%s): %s; backing off %.1fs",
                    self.__class__.__name__,
                    attempt,
                    self.max_retries,
                    exc,
                    wait_time,
                )
                if attempt == self.max_retries:
                    break
                time.sleep(wait_time)
        assert last_exc is not None
        raise last_exc

    def get_llm(self):
        from langchain_core.runnables import RunnableLambda

        provider = self
        return RunnableLambda(lambda prompt: provider.generate(_prompt_to_text(prompt)).text or "")

    def generate(self, prompt: str, *, stream: bool = False) -> LLMResponse:
        prompt = _prompt_to_text(prompt)
        prompt_tokens = self._guard_prompt(prompt)
        payload = self._payload(prompt, stream=stream)
        response = self._post(payload, stream=stream)

        usage = LLMUsage(prompt_tokens=prompt_tokens)

        if not stream:
            data = response.json()
            response.close()
            choices = data.get("choices", [])
            if not choices:
                raise ValueError("No choices returned from completion endpoint.")
            message = choices[0].get("message", {})
            text = message.get("content", "")
            completion_tokens = tokenize_len(text, encoding=self._tokenizer)
            usage.completion_tokens = completion_tokens
            if data.get("usage"):
                usage.prompt_tokens = data["usage"].get("prompt_tokens", prompt_tokens)
                usage.completion_tokens = data["usage"].get("completion_tokens", completion_tokens)
                usage.total_tokens = data["usage"].get("total_tokens")
            else:
                usage.total_tokens = (
                    (usage.prompt_tokens or 0) + (usage.completion_tokens or 0)
                )
            return LLMResponse(text=text, usage=usage, raw=data)

        buffer: list[str] = []

        def _iter() -> Iterator[str]:
            nonlocal usage
            try:
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    if line.startswith("data:"):
                        line = line[len("data:") :].strip()
                    if line in ("[DONE]", "[done]"):
                        break
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    choices = payload.get("choices", [])
                    if not choices:
                        continue
                    delta = choices[0].get("delta", {})
                    piece = delta.get("content")
                    if piece:
                        buffer.append(piece)
                        usage.completion_tokens = tokenize_len(
                            "".join(buffer),
                            encoding=self._tokenizer,
                        )
                        if usage.prompt_tokens is not None and usage.completion_tokens is not None:
                            usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
                        yield piece
                    if payload.get("usage"):
                        usage.prompt_tokens = payload["usage"].get("prompt_tokens", usage.prompt_tokens)
                        usage.completion_tokens = payload["usage"].get(
                            "completion_tokens", usage.completion_tokens
                        )
                        usage.total_tokens = payload["usage"].get("total_tokens", usage.total_tokens)
            finally:
                response.close()
                if usage.completion_tokens is None:
                    usage.completion_tokens = tokenize_len(
                        "".join(buffer),
                        encoding=self._tokenizer,
                    )
                if usage.prompt_tokens is not None and usage.completion_tokens is not None:
                    usage.total_tokens = usage.prompt_tokens + usage.completion_tokens

        return LLMResponse(stream=_iter(), usage=usage, raw=None, text=None)


class VLLMProvider(OpenAICompatibleHTTPProvider):
    """HTTP provider for vLLM's OpenAI-compatible server."""

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        tokenizer: Optional[str] = None,
        max_context_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        **generation_kwargs,
    ):
        base_url = base_url or os.environ.get("VLLM_BASE_URL", "http://127.0.0.1:8000")
        model = model or os.environ.get("VLLM_MODEL", "meta-llama/Llama-3-8B-Instruct")
        api_key = api_key or os.environ.get("VLLM_API_KEY")
        if max_context_tokens is None:
            try:
                max_context_tokens = int(os.environ.get("VLLM_MAX_CONTEXT", "8192"))
            except Exception:
                max_context_tokens = 8192
        super().__init__(
            base_url=base_url,
            model=model,
            api_key=api_key,
            system_prompt=system_prompt or os.environ.get("VLLM_SYSTEM_PROMPT"),
            tokenizer=tokenizer or os.environ.get("VLLM_TOKENIZER"),
            max_context_tokens=max_context_tokens,
            max_output_tokens=max_output_tokens,
            **generation_kwargs,
        )


class SGLangProvider(OpenAICompatibleHTTPProvider):
    """HTTP provider for SGLang (supports OpenAI-compatible endpoints)."""

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None,
        tokenizer: Optional[str] = None,
        max_context_tokens: Optional[int] = None,
        max_output_tokens: Optional[int] = None,
        **generation_kwargs,
    ):
        base_url = base_url or os.environ.get("SGLANG_BASE_URL", "http://127.0.0.1:30000")
        model = model or os.environ.get("SGLANG_MODEL", "deepseek-ai/DeepSeek-V2.5")
        api_key = api_key or os.environ.get("SGLANG_API_KEY")
        if max_context_tokens is None:
            try:
                max_context_tokens = int(os.environ.get("SGLANG_MAX_CONTEXT", "16384"))
            except Exception:
                max_context_tokens = 16384
        super().__init__(
            base_url=base_url,
            model=model,
            api_key=api_key,
            system_prompt=system_prompt or os.environ.get("SGLANG_SYSTEM_PROMPT"),
            tokenizer=tokenizer or os.environ.get("SGLANG_TOKENIZER"),
            max_context_tokens=max_context_tokens,
            max_output_tokens=max_output_tokens,
            **generation_kwargs,
        )


def get_llm_provider(provider_name: str = "llama_cpp", **kwargs) -> LLMProvider:
    """
    Factory function to get an LLM provider.
    """
    provider_name = provider_name.lower()
    if provider_name == "huggingface_api":
        return HuggingFaceAPIProvider(**kwargs)
    if provider_name == "llama_cpp":
        return LlamaCPPProvider(**kwargs)
    if provider_name in {"vllm", "vllm_api"}:
        return VLLMProvider(**kwargs)
    if provider_name in {"sglang", "sglang_api"}:
        return SGLangProvider(**kwargs)
    raise ValueError(f"Unknown LLM provider: {provider_name}")


# Backwards-compatibility alias for older imports
LlmProvider = LLMProvider


if __name__ == "__main__":
    try:
        provider = get_llm_provider()
        llm = provider.get_llm()
        logger.info("Successfully created LLM instance.")
    except ValueError as exc:
        logger.error(exc)
