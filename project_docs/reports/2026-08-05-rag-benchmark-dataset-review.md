# RAG Benchmark Dataset Review

This report records the dataset expansion used for RunPod model, GPU, prompt, retrieval, and
context-window comparisons.

## Summary

- Active blocking gate: `data/evaluation/acceptance/rag_v1_questions.jsonl`
- Raw generated candidates: `data/evaluation/acceptance/rag_v1_candidate_questions.generated.jsonl`
- Reviewed benchmark suite: `data/evaluation/acceptance/rag_v1_benchmark_questions.jsonl`
- Benchmark size: `91` rows
- Composition: `34` active gate rows plus `57` reviewed additions
- Decision: keep the 34-row gate blocking; use the 91-row suite as the frozen non-blocking
  comparison dataset.
- Baseline evidence: RunPod A40 `Qwen/Qwen2.5-7B-Instruct` vector run
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z` passed with `90` executed, `1` skipped,
  `0` failures, full-answer transcripts, and `promotion_ready=true`.

## Raw Generation Review

The deterministic drafter produced `100` schema-valid rows with no duplicate IDs/questions and no
blocked `docs/servicenow` paths. The raw output was not used as the frozen benchmark suite because
it skewed toward low-value Slurm man-page/admin fragments:

- `89` Slurm basics
- `6` research-data services
- `5` Amarel access
- `0` support-policy rows beyond incidental matches

The raw file is still useful as a first-pass source, but it needs review before use.

## Reviewed Benchmark Coverage

The reviewed suite has this category balance:

- `30` Slurm basics
- `29` Amarel access/storage
- `14` support/software policy
- `9` research-data services
- `8` negative safety
- `1` attachment optional

The reviewed additions cover user-facing procedures and troubleshooting: Slurm scripts, interactive
jobs, arrays, GPU directives, job monitoring, storage quotas, transfer tools, Open OnDemand/FastX,
community software, ownership, license review, research-data service selection, and safety refusals.

## Baseline Run

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/cloud_run_ledger.md`
- Plots:
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/plots/latency-by-question.svg`,
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/plots/ttft-by-question.svg`,
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/plots/source-counts-by-question.svg`
- Result: `90` pass, `0` fail, `1` skipped synthetic attachment row,
  `promotion_ready=true`.
- Manual-review rows: `39` advisory quality-review rows.
- p95 latency: `10773.45` ms.
- p95 time to first token: `861.33` ms.
- Runtime: `601.849 s`.
- Estimated cost: `$0.0718145704` from balance delta.

## Remaining Runs

Reuse exactly the same suite for the requested comparisons:

- RTX 4090 versus A40 cost/runtime
- `Qwen/Qwen2.5-14B-Instruct` versus the 7B baseline
- A100 and L40S GPU options
- one roughly 32B-class instruct model after the 14B/GPU baselines

No private ServiceNow task JSON, secrets, `.env` files, or raw private corpus should be uploaded for
these runs.
