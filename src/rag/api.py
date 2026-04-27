from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from src.rag.llm_provider import tokenize_len
from src.rag.logger import get_logger
from src.rag.service import (
    DEFAULT_GATEWAY_PROVIDER,
    RAGService,
    RAGServiceStream,
    extract_rag_sources,
    normalize_rag_answer,
)

logger = get_logger(__name__)

RAG_MODEL_ID = "oarc-rag-v1"
SSE_MEDIA_TYPE = "text/event-stream"


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
    rag_service: Optional[RAGService] = None,
    model_id: str = RAG_MODEL_ID,
) -> FastAPI:
    app = FastAPI(
        title="OARC RAG Gateway",
        version="0.1.0",
        description="OpenAI-compatible API boundary for the OARC RAG pipeline.",
    )
    app.state.rag_service = rag_service or RAGService(chain_factory=rag_chain_factory)
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
            **_get_rag_service(app).health(),
            "model": app.state.model_id,
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
                        **_get_rag_service(app).provider_metadata(),
                    },
                }
            ],
        }

    @app.post("/v1/chat/completions")
    def chat_completions(payload: ChatCompletionRequest) -> Any:
        try:
            question = extract_latest_user_question(payload.messages)
        except ValueError as exc:
            return _error_response(
                str(exc),
                status_code=422,
                error_type="invalid_request_error",
                param="messages",
            )

        if payload.stream:
            return _streaming_completion_response(
                service=_get_rag_service(app),
                question=question,
                model=app.state.model_id,
            )

        try:
            result = _get_rag_service(app).answer(question)
        except Exception:
            logger.exception("RAG gateway completion failed.")
            return _error_response(
                "The RAG gateway failed to generate a completion.",
                status_code=500,
                error_type="server_error",
            )

        return format_chat_completion_response(
            answer=result.answer,
            question=question,
            model=app.state.model_id,
            request_id=result.request_id,
            sources=result.sources,
            metadata=result.metadata,
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


def format_chat_completion_response(
    *,
    answer: str,
    question: str,
    model: str,
    request_id: str,
    sources: Optional[list[dict[str, Any]]] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    prompt_tokens = tokenize_len(question)
    completion_tokens = tokenize_len(answer)
    response = {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "rag_request_id": request_id,
        "rag_sources": sources or [],
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
    if metadata is not None:
        response["rag_metadata"] = _public_metadata(metadata)
    return response


def _streaming_completion_response(
    *,
    service: RAGService,
    question: str,
    model: str,
) -> StreamingResponse | JSONResponse:
    try:
        stream = service.start_stream(question)
    except Exception:
        logger.exception("RAG gateway completion failed before streaming started.")
        return _error_response(
            "The RAG gateway failed to generate a completion.",
            status_code=500,
            error_type="server_error",
        )

    return StreamingResponse(
        _iter_service_stream(service=service, stream=stream, model=model),
        media_type=SSE_MEDIA_TYPE,
    )


def _iter_service_stream(
    *,
    service: RAGService,
    stream: RAGServiceStream,
    model: str,
) -> Iterable[str]:
    completion_id = _chat_completion_id()
    created = int(time.time())
    answer_parts: list[str] = []
    yield _sse_data(_chat_chunk(completion_id, model, created, {"role": "assistant"}))

    try:
        for piece in stream.chunks:
            text = str(piece)
            if not text:
                continue
            answer_parts.append(text)
            yield _sse_data(_chat_chunk(completion_id, model, created, {"content": text}))
    except Exception as exc:
        logger.exception("RAG gateway streaming completion failed.")
        service.fail_stream(stream, exc)
        yield _sse_event(
            "error",
            {
                "error": {
                    "message": "The RAG gateway failed while streaming a completion.",
                    "type": "server_error",
                    "param": None,
                    "code": None,
                }
            },
        )
        yield "data: [DONE]\n\n"
        return

    metadata = service.finalize_stream(stream, "".join(answer_parts))
    yield _sse_data(
        _chat_chunk(
            completion_id,
            model,
            created,
            {},
            finish_reason="stop",
            request_id=stream.request_id,
            sources=stream.sources,
            metadata=metadata,
        )
    )
    yield "data: [DONE]\n\n"


def _chat_chunk(
    completion_id: str,
    model: str,
    created: int,
    delta: dict[str, Any],
    *,
    finish_reason: Optional[str] = None,
    request_id: Optional[str] = None,
    sources: Optional[list[dict[str, Any]]] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": delta,
                "finish_reason": finish_reason,
            }
        ],
    }
    if request_id is not None:
        chunk["rag_request_id"] = request_id
        chunk["rag_sources"] = sources or []
    if metadata is not None:
        chunk["rag_metadata"] = _public_metadata(metadata)
    return chunk


def _sse_data(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload, separators=(',', ':'))}\n\n"


def _sse_event(event: str, payload: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, separators=(',', ':'))}\n\n"


def _chat_completion_id() -> str:
    return f"chatcmpl-{uuid.uuid4().hex}"


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


def _public_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in metadata.items()
        if not key.startswith("_") and key not in {"retrieved_doc_ids"}
    }


def _get_rag_service(app: FastAPI) -> RAGService:
    return app.state.rag_service


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
    "extract_rag_sources",
    "extract_latest_user_question",
    "format_chat_completion_response",
    "normalize_rag_answer",
]
