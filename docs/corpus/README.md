# Corpus Layout

This directory organizes source documents for RAG ingestion by authority level so future corpus
expansion does not blur Amarel-specific guidance with third-party examples.

## Authority Levels

- `authoritative/`: Rutgers OARC and Amarel-specific materials. These should win when guidance
  conflicts with other sources.
- `reference/`: upstream software documentation such as Slurm, Apptainer, OpenMPI, CUDA, and
  similar vendor or project docs. These are valid for generic behavior, not site policy.
- `external/`: non-Rutgers materials such as other institutions' cluster guides and GitHub repos.
  These should be treated as examples or fallback references, not as Amarel policy.

## Recommended Placement Rules

- Put Amarel/OARC docs under `authoritative/amarel/`.
- Put upstream project docs under `reference/<project>/<version-or-scope>/`.
- Put other universities' guides under
  `external/institutions/<institution>/<cluster-or-site>/`.
- Put GitHub-derived docs under `external/github/<org>/<repo>/`.

Keep external names intact in filenames and content. Do not rename a third-party cluster to
"Amarel" in the source material. Alignment to Amarel should happen later through retrieval policy,
prompting, and answer synthesis.

## Current Runtime Note

The current loader still expects a single Markdown root via `DATA_PATH`. This tree is therefore the
authoritative source layout for future ingestion, while any combined runtime corpus should be built
from these directories in a controlled way.

## Suggested Workflow

1. Add or import raw Markdown into the appropriate subtree here.
2. Preserve provenance in the local `README.md` for that source bucket.
3. Build a curated combined corpus only after deciding which buckets should participate in a given
   index.
4. Keep Amarel docs and external docs in separate subtrees even if they are embedded into one
   vector store later.
