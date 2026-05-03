# Docs Index and Corpus Audit

This directory is primarily for RAG corpus material and a small number of supporting runbooks. The
canonical project architecture guide lives in
[`project_docs/ARCHITECTURE.md`](../project_docs/ARCHITECTURE.md), not in this directory.

Do not read, audit, rewrite, or use `docs/servicenow/task*json` files for documentation work. Raw
ServiceNow exports are handled by the ServiceNow preparation scripts and should not be treated as
general documentation.

## Architecture-Relevant Supporting Docs

- `docs/hpc-vllm-runbook.md`: operational runbook for hosted vLLM on HPC. This supports the
  deployment flow documented in `project_docs/ARCHITECTURE.md`.

## Corpus Material

- `docs/google_sites_guide/`: OARC/Amarel Google Sites guide Markdown used by default as
  `DATA_PATH`.
- `docs/slurm-23.02.7/`: vendored official Slurm 23.02.7 corpus.
  - `markdown/`: RAG-ready Markdown root.
  - `markdown/html/`: converted Slurm web docs.
  - `markdown/man/`: converted Slurm manpages.
  - `markdown/pdf/`: converted PDF companions.
  - `upstream/`: exact extracted upstream files for provenance and inspection.
  - `rendered/`: SSI-expanded browseable HTML, not the Markdown ingestion tree.
- `docs/corpus/`: authority-tiered future corpus layout.
  - `authoritative/`: Rutgers OARC and Amarel-specific materials.
  - `reference/`: upstream software documentation such as Slurm.
  - `external/`: non-Rutgers examples and supplementary references.
  - `staging/`: temporary generated corpus builds.

## Miscellaneous or Supporting Docs

- `docs/onboarding/`: user-facing HPC onboarding material. Preserve it, but do not treat it as the
  canonical code architecture source.

If a document appears important but its relationship to the codebase is unclear, leave it in place
and add an audit note here instead of deleting or moving it.

## Recommended RAG Roots

- OARC guide only: `docs/google_sites_guide`
- Slurm 23.02.7 full corpus: `docs/slurm-23.02.7/markdown`
- Slurm web docs only: `docs/slurm-23.02.7/markdown/html`
- Slurm manpages only: `docs/slurm-23.02.7/markdown/man`
- Slurm PDF companions only: `docs/slurm-23.02.7/markdown/pdf`

The current loader in `src/rag/data_loader.py` ingests Markdown from `DATA_PATH`, so the Slurm
`markdown/` tree is the correct root for that corpus. Prepared ServiceNow JSONL, when approved for
a run, is configured separately with `SERVICE_NOW_DATA_PATH`.

## Do Not Use These Paths As `DATA_PATH`

- `docs/slurm-23.02.7/upstream`: exact upstream source files, not the ingestion tree.
- `docs/slurm-23.02.7/rendered`: browseable rendered HTML, not the ingestion tree.
- `docs/servicenow`: handled separately through `SERVICE_NOW_DATA_PATH`.
- `docs/`: only use the whole tree if you intentionally want every Markdown file here mixed into
  one corpus.

## Future Documentation Placement

- Project architecture, script contracts, test strategy, and maintenance policy:
  `project_docs/ARCHITECTURE.md`.
- Product and implementation plans: `.plans/`.
- Corpus provenance and RAG source placement: local README files under `docs/`.
- Operational runbooks that directly support corpus/runtime operations may remain in `docs/`, but
  should link back to `project_docs/ARCHITECTURE.md` rather than duplicating architecture details.

## Recommended Local Test Environment

Primary workflow:

```bash
uv sync --extra dev
source .venv/bin/activate
python -m pytest tests/unit/test_slurm_docs.py -q
python -m ruff check src/rag/slurm_docs.py scripts/rag/import_slurm_docs.py tests/unit/test_slurm_docs.py
```

If you already maintain a separate conda environment for local validation, treat that as a fallback
rather than the default workflow.
