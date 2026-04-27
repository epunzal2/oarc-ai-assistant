from __future__ import annotations

import os
import time
import uuid
from collections.abc import Callable, Sequence
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from src.rag import config
from src.rag.llm_provider import tokenize_len
from src.rag.logger import get_logger

logger = get_logger(__name__)

RAG_MODEL_ID = "oarc-rag-v1"
DEFAULT_GATEWAY_PROVIDER = "vllm"
DEFAULT_VECTOR_STORE = "qdrant"


class ChatMessage(BaseModel):
    role: str
    content: Any

    model_config = ConfigDict(extra="allow")


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    stream: bool = False

    model_config = ConfigDict(extra="allow")


def create_app(
    *,
    rag_chain_factory: Optional[Callable[[], Any]] = None,
    model_id: str = RAG_MODEL_ID,
) -> FastAPI:
    app = FastAPI(
        title="OARC RAG Gateway",
        version="0.1.0",
        description="OpenAI-compatible API boundary for the OARC RAG pipeline.",
    )
    app.state.rag_chain_factory = rag_chain_factory or _default_rag_chain_factory
    app.state.rag_chain = None
    app.state.model_id = model_id

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
        message = "Invalid request."
        if exc.errors():
            message = f"Invalid request: {exc.errors()[0].get('msg', message)}"
        return _error_response(
            message,
            status_code=422,
            error_type="invalid_request_error",
        )

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "rag-gateway",
            "model": app.state.model_id,
            "backend": _vllm_metadata(),
        }

    @app.get("/v1/models")
    def models() -> dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {
                    "id": app.state.model_id,
                    "object": "model",
                    "created": 0,
                    "owned_by": "oarc",
                    "metadata": {
                        "rag": True,
                        "backing_provider": DEFAULT_GATEWAY_PROVIDER,
                        **_vllm_metadata(),
                    },
                }
            ],
        }

    @app.post("/v1/chat/completions")
    def chat_completions(payload: ChatCompletionRequest) -> Any:
        if payload.stream:
            return _error_response(
                "Streaming chat completions are not supported by this gateway phase.",
                status_code=400,
                error_type="invalid_request_error",
                param="stream",
                code="streaming_unsupported",
            )

        try:
            question = extract_latest_user_question(payload.messages)
        except ValueError as exc:
            return _error_response(
                str(exc),
                status_code=422,
                error_type="invalid_request_error",
                param="messages",
            )

        try:
            result = _get_rag_chain(app).invoke(question)
        except Exception:
            logger.exception("RAG gateway completion failed.")
            return _error_response(
                "The RAG gateway failed to generate a completion.",
                status_code=500,
                error_type="server_error",
            )

        answer = normalize_rag_answer(result)
        return format_chat_completion_response(
            answer=answer,
            question=question,
            model=app.state.model_id,
        )

    return app


def extract_latest_user_question(messages: Sequence[ChatMessage]) -> str:
    for message in reversed(messages):
        if message.role != "user":
            continue
        text = _content_to_text(message.content)
        if text:
            return text
    raise ValueError("messages must include a non-empty user message")


def normalize_rag_answer(result: Any) -> str:
    if isinstance(result, dict) and "answer" in result:
        answer = result.get("answer")
        return "" if answer is None else str(answer)
    return "" if result is None else str(result)


def format_chat_completion_response(
    *,
    answer: str,
    question: str,
    model: str,
) -> dict[str, Any]:
    prompt_tokens = tokenize_len(question)
    completion_tokens = tokenize_len(answer)
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


def _default_rag_chain_factory() -> Any:
    from src.rag.rag_pipeline import create_rag_chain

    provider_name = os.environ.get("RAG_GATEWAY_LLM_PROVIDER", DEFAULT_GATEWAY_PROVIDER)
    vector_store_type = os.environ.get("RAG_GATEWAY_VECTOR_STORE", DEFAULT_VECTOR_STORE)
    return create_rag_chain(
        llm_provider_name=provider_name,
        vector_store_type=vector_store_type,
    )


def _get_rag_chain(app: FastAPI) -> Any:
    if app.state.rag_chain is None:
        app.state.rag_chain = app.state.rag_chain_factory()
    return app.state.rag_chain


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
                continue
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            text = item.get("text")
            if (item_type is None or item_type == "text") and isinstance(text, str):
                parts.append(text)
        return "\n".join(part.strip() for part in parts if part.strip()).strip()
    return ""


def _vllm_metadata() -> dict[str, Any]:
    provider_kwargs = config.provider_kwargs(DEFAULT_GATEWAY_PROVIDER)
    return {
        "backing_model": provider_kwargs.get("model"),
        "backing_base_url": provider_kwargs.get("base_url"),
        "backing_health_url": config.provider_health_url(DEFAULT_GATEWAY_PROVIDER),
    }


def _error_response(
    message: str,
    *,
    status_code: int,
    error_type: str,
    param: Optional[str] = None,
    code: Optional[str] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "type": error_type,
                "param": param,
                "code": code,
            }
        },
    )


app = create_app()

__all__ = [
    "RAG_MODEL_ID",
    "app",
    "create_app",
    "extract_latest_user_question",
    "format_chat_completion_response",
    "normalize_rag_answer",
]
