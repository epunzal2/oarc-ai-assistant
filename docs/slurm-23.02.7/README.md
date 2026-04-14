# Slurm 23.02.7 Corpus

This directory vendors the official Slurm 23.02.7 documentation for local retrieval and offline inspection.

## Provenance
- Source archive: https://download.schedmd.com/slurm/slurm-23.02.7.tar.bz2
- Imported at: 2026-03-27T20:25:02.659649+00:00
- Archive SHA256: `eba6db8990abf40402d8e30d8706a7ddd0560e0e307c567f0fb72f1c8a522078`
- Archive size: 7447239 bytes

## Layout
- `upstream/html` and `upstream/man`: exact extracted upstream docs
- `rendered/html`: SSI-expanded browseable HTML
- `markdown/html`, `markdown/man`, `markdown/pdf`: Markdown corpus for the loader
- `manifest.json`: import metadata and counts

## Counts
- Web docs: 114 (111 HTML pages + 3 PDFs)
- Man pages: 41
- Raw upstream HTML files: 161
- Raw upstream man files: 50

## Using This Corpus
- Runtime: `DATA_PATH=docs/slurm-23.02.7/markdown`
- Evaluation: set `dataset.document_source.markdown_dir: "docs/slurm-23.02.7/markdown"`
- The default corpus remains `docs/google_sites_guide`.

## Rebuild Command
- `python scripts/rag/import_slurm_docs.py --version 23.02.7 --output-dir docs/slurm-23.02.7 --force`
