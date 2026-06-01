"""OpenAI-compatible HTTP boundary for the OARC RAG service.

This module intentionally owns only request validation, response formatting, and
streaming wire shape. Retrieval, prompt construction, provider calls, source
extraction, and telemetry stay behind `RAGService` so UI/API tests can use fake
chains without initializing vector stores or model backends.
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from collections.abc import Callable, Iterable, Sequence
from io import BytesIO
from pathlib import Path
from typing import Any, Optional
from urllib.parse import unquote

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
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
UI_STATIC_DIR = Path(__file__).resolve().parent / "ui_static"
UI_INDEX_PATH = UI_STATIC_DIR / "index.html"
ATTACHMENT_MAX_BYTES = 5 * 1024 * 1024
ATTACHMENT_MAX_TEXT_CHARS = 60_000
ATTACHMENT_TOTAL_TEXT_CHARS = 80_000
ATTACHMENT_MAX_COUNT = 3
ATTACHMENT_MAX_PDF_PAGES = 25
ATTACHMENT_TEXT_EXTENSIONS = {".txt", ".md", ".markdown"}
ATTACHMENT_PDF_EXTENSIONS = {".pdf"}
ATTACHMENTS_DISABLED_MESSAGE = (
    "file attachments are disabled for this deployment; set "
    "RAG_UI_ATTACHMENTS_ENABLED=true only for private tunnel testing"
)


class ChatMessage(BaseModel):
    """Subset of OpenAI chat message fields consumed by the gateway."""

    role: str
    content: Any

    model_config = ConfigDict(extra="allow")


class RAGAttachment(BaseModel):
    """Ephemeral text extracted from a user-attached file for one chat request."""

    name: str = Field(min_length=1, max_length=255)
    mime_type: str = Field(default="", max_length=100)
    text: str = Field(min_length=1, max_length=ATTACHMENT_MAX_TEXT_CHARS)

    model_config = ConfigDict(extra="allow")


class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request with extension fields allowed."""

    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    stream: bool = False
    rag_attachments: list[RAGAttachment] = Field(
        default_factory=list,
        max_length=ATTACHMENT_MAX_COUNT,
    )

    model_config = ConfigDict(extra="allow")


def create_app(
    *,
    rag_chain_factory: Optional[Callable[[], Any]] = None,
    rag_service: Optional[RAGService] = None,
    model_id: str = RAG_MODEL_ID,
    ui_attachments_enabled: Optional[bool] = None,
) -> FastAPI:
    """Create the FastAPI app with injectable RAG dependencies for tests."""

    app = FastAPI(
        title="OARC RAG Gateway",
        version="0.1.0",
        description="OpenAI-compatible API boundary for the OARC RAG pipeline.",
    )
    app.state.rag_service = rag_service or RAGService(chain_factory=rag_chain_factory)
    app.state.model_id = model_id
    app.state.ui_attachments_enabled = (
        ui_attachments_enabled
        if ui_attachments_enabled is not None
        else _env_bool("RAG_UI_ATTACHMENTS_ENABLED", default=False)
    )
    app.mount(
        "/ui-static",
        StaticFiles(directory=UI_STATIC_DIR),
        name="ui-static",
    )

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

    @app.get("/", include_in_schema=False)
    def root() -> RedirectResponse:
        return RedirectResponse(url="/ui")

    @app.get("/ui", include_in_schema=False)
    def ui() -> FileResponse:
        return FileResponse(UI_INDEX_PATH)

    @app.post("/ui/attachments/extract", include_in_schema=False, response_model=None)
    async def extract_attachment(request: Request) -> Any:
        if not _ui_attachments_enabled(app):
            return _error_response(
                ATTACHMENTS_DISABLED_MESSAGE,
                status_code=403,
                error_type="forbidden",
                param="attachment",
            )
        try:
            content_length = request.headers.get("content-length")
            if content_length:
                try:
                    declared_size = int(content_length)
                except ValueError:
                    raise ValueError("invalid attachment size") from None
                if declared_size > ATTACHMENT_MAX_BYTES:
                    raise ValueError("attached file is too large")
            return extract_attachment_payload(
                await request.body(),
                filename=request.headers.get("x-attachment-name", ""),
                content_type=request.headers.get("content-type", ""),
            )
        except ValueError as exc:
            return _error_response(
                str(exc),
                status_code=422,
                error_type="invalid_request_error",
                param="attachment",
            )

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            **_get_rag_service(app).health(),
            "model": app.state.model_id,
            "ui": ui_capabilities(app),
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

        if payload.rag_attachments and not _ui_attachments_enabled(app):
            return _error_response(
                ATTACHMENTS_DISABLED_MESSAGE,
                status_code=403,
                error_type="forbidden",
                param="rag_attachments",
            )

        try:
            question = question_with_attachments(question, payload.rag_attachments)
        except ValueError as exc:
            return _error_response(
                str(exc),
                status_code=422,
                error_type="invalid_request_error",
                param="rag_attachments",
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
    """Return the latest non-empty user text from OpenAI-style chat messages."""

    for message in reversed(messages):
        if message.role != "user":
            continue
        text = _content_to_text(message.content)
        if text:
            return text
    raise ValueError("messages must include a non-empty user message")


def ui_capabilities(app: FastAPI) -> dict[str, Any]:
    """Return public browser UI capabilities and privacy-relevant limits."""

    return {
        "attachments_enabled": _ui_attachments_enabled(app),
        "attachment_limits": {
            "max_files": ATTACHMENT_MAX_COUNT,
            "max_bytes_per_file": ATTACHMENT_MAX_BYTES,
            "max_chars_per_file": ATTACHMENT_MAX_TEXT_CHARS,
            "max_chars_per_request": ATTACHMENT_TOTAL_TEXT_CHARS,
            "max_pdf_pages": ATTACHMENT_MAX_PDF_PAGES,
            "allowed_extensions": sorted(
                ATTACHMENT_TEXT_EXTENSIONS | ATTACHMENT_PDF_EXTENSIONS
            ),
        },
        "attachment_policy": (
            "Attachments are sent to this gateway for one request only. Use non-sensitive "
            "files unless this private tunnel deployment is approved for the data."
        ),
    }


def question_with_attachments(question: str, attachments: Sequence[RAGAttachment]) -> str:
    """Append ephemeral attachment excerpts to the question sent into the RAG chain."""

    if not attachments:
        return question

    total_chars = 0
    blocks: list[str] = []
    for index, attachment in enumerate(attachments, start=1):
        name = _safe_attachment_name(attachment.name)
        text = _clean_attachment_text(attachment.text)
        if not text:
            continue
        total_chars += len(text)
        if total_chars > ATTACHMENT_TOTAL_TEXT_CHARS:
            raise ValueError("attached file text is too large for one request")
        blocks.append(
            "\n".join(
                [
                    f"[Attachment {index}: {name}]",
                    text,
                ]
            )
        )

    if not blocks:
        return question

    return "\n\n".join(
        [
            "User question:",
            question,
            (
                "Request-scoped attachment excerpts. Treat these excerpts as context for this "
                "answer when they are relevant. They are not repository RAG sources; cite "
                "repository RAG sources separately when available."
            ),
            *blocks,
        ]
    )


def extract_attachment_payload(
    content: bytes,
    *,
    filename: str,
    content_type: str = "",
) -> dict[str, Any]:
    """Extract text from one uploaded UI attachment without persisting the file."""

    if not content:
        raise ValueError("attached file is empty")
    if len(content) > ATTACHMENT_MAX_BYTES:
        raise ValueError("attached file is too large")

    name = _safe_attachment_name(unquote(filename or "attachment"))
    suffix = Path(name).suffix.lower()
    media_type = _content_type_without_params(content_type)

    if suffix in ATTACHMENT_PDF_EXTENSIONS or (not suffix and media_type == "application/pdf"):
        text = _extract_pdf_text(content)
        kind = "pdf"
    elif (
        suffix in ATTACHMENT_TEXT_EXTENSIONS
        or (not suffix and media_type in {"text/plain", "text/markdown", ""})
    ):
        text = _decode_text_attachment(content)
        kind = "text"
    else:
        raise ValueError("unsupported attachment type; use .txt, .md, or .pdf")

    text = _clean_attachment_text(text)
    if not text:
        raise ValueError("attached file did not contain extractable text")

    truncated = len(text) > ATTACHMENT_MAX_TEXT_CHARS
    if truncated:
        text = text[:ATTACHMENT_MAX_TEXT_CHARS].rstrip()

    return {
        "name": name,
        "mime_type": media_type or "application/octet-stream",
        "kind": kind,
        "bytes": len(content),
        "chars": len(text),
        "truncated": truncated,
        "text": text,
    }


def format_chat_completion_response(
    *,
    answer: str,
    question: str,
    model: str,
    request_id: str,
    sources: Optional[list[dict[str, Any]]] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Format a non-streaming completion response with RAG extension fields."""

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
    """Start an SSE response or return JSON if setup fails before streaming."""

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
    """Yield OpenAI-style SSE chunks and finalize telemetry after the stream ends."""

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
    """Normalize supported OpenAI content shapes to plain user text."""

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


def _safe_attachment_name(name: str) -> str:
    filename = Path(name or "attachment").name.strip()
    filename = re.sub(r"[\x00-\x1f\x7f]+", "", filename)
    return filename[:255] or "attachment"


def _content_type_without_params(content_type: str) -> str:
    return content_type.split(";", 1)[0].strip().lower()


def _decode_text_attachment(content: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def _extract_pdf_text(content: bytes) -> str:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover - import failure depends on environment
        raise ValueError("PDF attachment support is unavailable") from exc

    try:
        reader = PdfReader(BytesIO(content))
        page_text = []
        for index, page in enumerate(reader.pages):
            if index >= ATTACHMENT_MAX_PDF_PAGES:
                break
            page_text.append(page.extract_text() or "")
    except Exception as exc:
        raise ValueError("PDF text extraction failed") from exc
    return "\n\n".join(page_text)


def _clean_attachment_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    normalized = re.sub(r"[ \t]+\n", "\n", normalized)
    normalized = re.sub(r"\n{4,}", "\n\n\n", normalized)
    return normalized.strip()


def _public_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Remove private fields before exposing request metadata to API clients."""

    return {
        key: value
        for key, value in metadata.items()
        if not key.startswith("_") and key not in {"retrieved_doc_ids"}
    }


def _get_rag_service(app: FastAPI) -> RAGService:
    return app.state.rag_service


def _ui_attachments_enabled(app: FastAPI) -> bool:
    return bool(getattr(app.state, "ui_attachments_enabled", False))


def _env_bool(name: str, *, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


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
    "UI_INDEX_PATH",
    "UI_STATIC_DIR",
    "app",
    "create_app",
    "extract_attachment_payload",
    "extract_rag_sources",
    "extract_latest_user_question",
    "format_chat_completion_response",
    "normalize_rag_answer",
    "question_with_attachments",
    "ui_capabilities",
]
