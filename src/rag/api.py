from __future__ import annotations

import os
import json
import time
import uuid
from collections.abc import Callable, Iterable, Sequence
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from src.rag import config
from src.rag.llm_provider import tokenize_len
from src.rag.logger import get_logger

logger = get_logger(__name__)

RAG_MODEL_ID = "oarc-rag-v1"
DEFAULT_GATEWAY_PROVIDER = "vllm"
DEFAULT_VECTOR_STORE = "qdrant"
SSE_MEDIA_TYPE = "text/event-stream"
SOURCE_SNIPPET_CHARS = 280


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
            chain = _get_rag_chain(app)
        except Exception:
            logger.exception("RAG gateway initialization failed.")
            return _error_response(
                "The RAG gateway failed to initialize the RAG pipeline.",
                status_code=500,
                error_type="server_error",
            )

        request_id = f"rag-{uuid.uuid4().hex}"

        if payload.stream:
            return _streaming_completion_response(
                chain=chain,
                question=question,
                model=app.state.model_id,
                request_id=request_id,
            )

        try:
            result = chain.invoke(question)
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
            request_id=request_id,
            sources=extract_rag_sources(result),
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


def extract_rag_sources(result: Any) -> list[dict[str, Any]]:
    if not isinstance(result, dict):
        return []

    sources: list[dict[str, Any]] = []
    seen: set[str] = set()
    for doc in result.get("context") or []:
        source = _source_from_doc(doc)
        if not source:
            continue
        dedupe_key = (
            source.get("chunk_id")
            or source.get("id")
            or source.get("source")
            or source.get("snippet")
        )
        if dedupe_key:
            key = str(dedupe_key)
            if key in seen:
                continue
            seen.add(key)
        sources.append(source)
    return sources


def format_chat_completion_response(
    *,
    answer: str,
    question: str,
    model: str,
    request_id: str,
    sources: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    prompt_tokens = tokenize_len(question)
    completion_tokens = tokenize_len(answer)
    return {
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


def _streaming_completion_response(
    *,
    chain: Any,
    question: str,
    model: str,
    request_id: str,
) -> StreamingResponse | JSONResponse:
    stream_answer = getattr(chain, "stream_answer", None)
    if callable(stream_answer):
        return StreamingResponse(
            _iter_live_stream(
                stream_answer=stream_answer,
                question=question,
                model=model,
                request_id=request_id,
            ),
            media_type=SSE_MEDIA_TYPE,
        )

    try:
        result = chain.invoke(question)
    except Exception:
        logger.exception("RAG gateway completion failed before streaming started.")
        return _error_response(
            "The RAG gateway failed to generate a completion.",
            status_code=500,
            error_type="server_error",
        )

    return StreamingResponse(
        _iter_completed_stream(
            answer=normalize_rag_answer(result),
            sources=extract_rag_sources(result),
            model=model,
            request_id=request_id,
        ),
        media_type=SSE_MEDIA_TYPE,
    )


def _iter_live_stream(
    *,
    stream_answer: Callable[[str], Any],
    question: str,
    model: str,
    request_id: str,
) -> Iterable[str]:
    completion_id = _chat_completion_id()
    created = int(time.time())
    yield _sse_data(_chat_chunk(completion_id, model, created, {"role": "assistant"}))

    chunks: Iterable[str] = []
    context: list[Any] = []
    answer_parts: list[str] = []
    try:
        stream_result = stream_answer(question)
        context = list(stream_result.get("context") or []) if isinstance(stream_result, dict) else []
        if isinstance(stream_result, dict):
            chunks = stream_result.get("chunks") or []
        else:
            chunks = stream_result
        for piece in chunks:
            text = str(piece)
            if not text:
                continue
            answer_parts.append(text)
            yield _sse_data(_chat_chunk(completion_id, model, created, {"content": text}))
    except Exception:
        logger.exception("RAG gateway streaming completion failed.")
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

    sources = extract_rag_sources({"context": context})
    yield _sse_data(
        _chat_chunk(
            completion_id,
            model,
            created,
            {},
            finish_reason="stop",
            request_id=request_id,
            sources=sources,
        )
    )
    yield "data: [DONE]\n\n"


def _iter_completed_stream(
    *,
    answer: str,
    sources: list[dict[str, Any]],
    model: str,
    request_id: str,
) -> Iterable[str]:
    completion_id = _chat_completion_id()
    created = int(time.time())
    yield _sse_data(_chat_chunk(completion_id, model, created, {"role": "assistant"}))
    if answer:
        yield _sse_data(_chat_chunk(completion_id, model, created, {"content": answer}))
    yield _sse_data(
        _chat_chunk(
            completion_id,
            model,
            created,
            {},
            finish_reason="stop",
            request_id=request_id,
            sources=sources,
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
    return chunk


def _sse_data(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload, separators=(',', ':'))}\n\n"


def _sse_event(event: str, payload: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, separators=(',', ':'))}\n\n"


def _chat_completion_id() -> str:
    return f"chatcmpl-{uuid.uuid4().hex}"


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


def _source_from_doc(doc: Any) -> dict[str, Any]:
    metadata = getattr(doc, "metadata", {}) or {}
    page_content = getattr(doc, "page_content", "") or ""
    source: dict[str, Any] = {}

    field_map = {
        "id": ("id", "document_id", "doc_id"),
        "source": ("source", "path", "file_path"),
        "title": ("title", "name"),
        "url": ("url", "source_url"),
        "chunk_id": ("chunk_id",),
        "score": ("score", "relevance_score"),
    }
    for output_key, metadata_keys in field_map.items():
        value = _first_metadata_value(metadata, metadata_keys)
        if value is not None and value != "":
            source[output_key] = value

    snippet = " ".join(str(page_content).split())[:SOURCE_SNIPPET_CHARS]
    if snippet:
        source["snippet"] = snippet
    return source


def _first_metadata_value(metadata: dict[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        value = metadata.get(key)
        if value is not None and value != "":
            return value
    return None


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
    "extract_rag_sources",
    "extract_latest_user_question",
    "format_chat_completion_response",
    "normalize_rag_answer",
]
