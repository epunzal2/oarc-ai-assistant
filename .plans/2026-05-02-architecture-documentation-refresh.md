Title: Architecture documentation refresh
Status: Done
Owner: agent-llm
Reviewers: n/a
Issues: n/a
Scope: repo-wide
Risk: medium

# Context & Problem

The repository has working RAG, evaluation, deployment, and telemetry code, but the current
architecture documentation is split between an early proposal in `architecture/`, phase-specific
plans, `README.md`, and `project_docs/DESIGN.md`. Some entries are stale or point to locations that
are no longer canonical.

New engineers need a single verified project architecture reference that explains the current code,
script entrypoints, tests, operations, docs layout, and maintenance expectations without mixing
project documentation into the RAG corpus under `docs/`.

# Goals / Non-goals

- Create `project_docs/ARCHITECTURE.md` as the canonical current architecture guide.
- Keep `docs/` focused on corpus material and operational runbooks; add an index/audit rather than
  reorganizing corpus files.
- Update stale architecture links and documentation references.
- Improve concise docstrings and inline comments in `src/`, `scripts/`, and `tests/` where they
  clarify contracts, side effects, invariants, or external integrations.
- Do not read or modify `docs/servicenow/task*json`.
- Do not rewrite application behavior except to make comments/docstrings accurate.

# Design Overview

`project_docs/ARCHITECTURE.md` will be the canonical project-facing document. It will summarize the
runtime RAG gateway, direct chat harnesses, corpus/index build path, hosted vLLM workflow,
evaluation bakeoff, MLflow/telemetry, tests, scripts, and documentation ownership.

`architecture/architecture.md` will become a compatibility pointer to avoid preserving a stale
proposal as if it were current. Other legacy `architecture/` files are left in place unless they are
clearly contradicted by current code.

# Implementation Plan

- [x] Create this plan under `.plans/`.
- [x] Add `project_docs/ARCHITECTURE.md`.
- [x] Replace `architecture/architecture.md` with a compatibility pointer.
- [x] Update `README.md` architecture links, stale references, and maintenance checklist language.
- [x] Update `docs/README.md` with a docs index/audit and ServiceNow task JSON exclusion note.
- [x] Add high-signal docstrings/comments in `src/`, `scripts/`, and `tests/`.
- [x] Run targeted and full unit tests, lint when available, and link checks.

# Data Model & Migrations

No schema, storage, or runtime data model changes are planned.

# Testing Strategy

- `python -m pytest tests/unit -q`
- `python -m pytest tests/unit/test_rag_gateway.py tests/unit/test_rag_service_hardening.py -q`
- `python -m pytest tests/unit/test_slurm_docs.py -q`
- `python -m ruff check src scripts tests` when Ruff is installed
- Shell link/path checks for new documentation references, excluding `docs/servicenow/task*json`

# Rollout & Telemetry

This is a documentation-only change. No runtime rollout or telemetry changes are required.

# Risks & Mitigations

- Risk: duplicating content across README and architecture docs.
  Mitigation: keep README as quickstart and link to the canonical architecture doc.
- Risk: accidentally treating corpus docs as project docs.
  Mitigation: `docs/README.md` explicitly classifies corpus, supporting, and project-doc paths.
- Risk: touching restricted ServiceNow task JSON.
  Mitigation: exclude those files from all searches and edits.

# Security & Privacy

The change documents existing privacy controls: prompt hashing, MLflow artifact caps, and
ServiceNow task JSON handling. It does not expose raw ServiceNow records.

# Docs to Update

- `project_docs/ARCHITECTURE.md`
- `architecture/architecture.md`
- `README.md`
- `docs/README.md`
- Selected inline docstrings/comments in `src/`, `scripts/`, and `tests/`

# Rollback Plan

Revert the documentation and comment/docstring changes. No runtime state rollback is needed.

# Decision Log

- 2026-05-02: Initial executing plan created by agent-llm.
- 2026-05-02: Completed canonical architecture documentation, docs audit, inline documentation
  refresh, tests, Ruff, and link verification.

# Outcome

Added `project_docs/ARCHITECTURE.md` as the canonical architecture guide, converted the stale
`architecture/architecture.md` proposal into a pointer, refreshed README and `docs/README.md`, and
improved high-signal docstrings/comments across the runtime, evaluation, script, and test surfaces.
