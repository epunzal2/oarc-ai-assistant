Title: assistant-ui gateway chat surface
Status: Executing
Owner: agent-llm
Reviewers: n/a
Issues: n/a
Scope: package:rag
Risk: medium

# Context & Problem

The gateway-hosted chat UI needs to look and behave more like a modern AI lab chat surface while
preserving OARC-specific source and request metadata. The existing no-build UI proved the endpoint
contract, but it is becoming costly to extend compared with a purpose-built chat component library.

# Goals / Non-goals

- Use `@assistant-ui/react` for the browser thread and composer.
- Keep the public FastAPI routes unchanged: `/ui`, `/ui-static/*`, `/health`, `/v1/models`, and
  `/v1/chat/completions`.
- Preserve source and metadata visibility for every completed RAG answer.
- Keep attachment text request-scoped and disabled unless `RAG_UI_ATTACHMENTS_ENABLED=true`.
- Do not add auth, transcript persistence, a new UI service, or direct browser access to vLLM,
  FAISS, or Qdrant.

# Design Overview

The UI source lives under `src/rag/ui_app/` and compiles with Vite into `src/rag/ui_static/`. The
React app uses assistant-ui primitives with a custom `useLocalRuntime` adapter that sends
same-origin OpenAI-style streaming requests. The final SSE chunk provides `rag_request_id`,
`rag_sources`, and `rag_metadata`, which the app stores in assistant message metadata and the side
inspector.

# Implementation Plan

- [x] Add pinned npm dependencies and a reproducible Vite build.
- [x] Implement the assistant-ui thread, composer, status header, attachments, and source inspector.
- [x] Add explicit RunPod attachment-test support and generated UI sample attachment.
- [x] Keep FastAPI serving the same built static asset paths.
- [x] Add local browser screenshots for desktop and mobile.
- [x] Capture one live RunPod UI screenshot and terminate the pod.
- [ ] Compare follow-up LLM performance and accuracy runs.

# Testing Strategy

- `npm run check:ui`
- `npm run build:ui`
- Gateway contract tests for `/ui` and `/ui-static/*`.
- Playwright browser smoke screenshots against the served FastAPI UI.
- RunPod browser screenshot after one non-sensitive live chat question.

# Security & Privacy

The UI calls only same-origin gateway endpoints. Attachment extraction keeps existing server limits
and remains disabled unless explicitly enabled. No API keys, provider tokens, private ServiceNow
exports, or raw persistent transcripts are added to the browser bundle.

# Rollback Plan

Revert the Vite/assistant-ui source and restore the previous `src/rag/ui_static/` static assets. The
OpenAI-compatible API contract remains unchanged.

# Decision Log

- 2026-08-04: Chose assistant-ui with a custom OpenAI-compatible SSE adapter so the UI can use a
  legal chat template library while retaining OARC source/metadata rendering.
