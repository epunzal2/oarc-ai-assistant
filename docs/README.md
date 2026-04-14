# Docs Paths

This directory contains several documentation trees, but not every path here should be used as a RAG
corpus root.

## Use These Paths For RAG

- OARC guide only: `docs/google_sites_guide`
- Slurm 23.02.7 full corpus: `docs/slurm-23.02.7/markdown`
- Slurm web docs only: `docs/slurm-23.02.7/markdown/html`
- Slurm manpages only: `docs/slurm-23.02.7/markdown/man`
- Slurm PDF companions only: `docs/slurm-23.02.7/markdown/pdf`

The current loader in `src/rag/data_loader.py` only ingests Markdown from `DATA_PATH`, so the Slurm
`markdown/` tree is the correct root for that corpus.

## Do Not Use These Paths As `DATA_PATH`

- `docs/slurm-23.02.7/upstream`
  - Exact extracted upstream files for provenance and inspection.
- `docs/slurm-23.02.7/rendered`
  - SSI-expanded browseable HTML, not the Markdown ingestion tree.
- `docs/servicenow`
  - ServiceNow content is handled separately through `SERVICE_NOW_DATA_PATH`, not `DATA_PATH`.
- `docs/`
  - Only use the whole `docs/` tree if you intentionally want every Markdown file here mixed into one
    corpus.

## ServiceNow Path

If you want the prepared ServiceNow corpus in the same run, keep `SERVICE_NOW_DATA_PATH` pointed at:

- `docs/servicenow/task_prepared.jsonl`

This is additive to the Markdown corpus path above.

## Recommended Local Test Environment

On this machine, `python -m pytest` in the Conda `base` environment segfaults during runner startup.
The working local path is the `hpc-analytics` environment:

```bash
conda run -n hpc-analytics python -m pytest tests/unit/test_slurm_docs.py -q
conda run -n hpc-analytics ruff check src/rag/slurm_docs.py scripts/rag/import_slurm_docs.py tests/unit/test_slurm_docs.py
```

If `hpc-analytics` does not already have the repo test tools, install them there:

```bash
conda run -n hpc-analytics python -m pip install pytest pytest-cov ruff
conda run -n hpc-analytics python -m pip install beautifulsoup4 pypdf requests
conda run -n hpc-analytics python -m pip install -e .
```
