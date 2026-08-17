# RAG Benchmark Dataset Review

This report records the dataset expansion used for RunPod model, GPU, prompt, retrieval, and
context-window comparisons.

## Summary

- Active blocking gate: `data/evaluation/acceptance/rag_v1_questions.jsonl`
- Raw generated candidates: `data/evaluation/acceptance/rag_v1_candidate_questions.generated.jsonl`
- Reviewed benchmark suite: `data/evaluation/acceptance/rag_v1_benchmark_questions.jsonl`
- Benchmark size: `100` executed non-attachment rows
- Composition: `34` active gate rows plus `66` reviewed additions
- Decision: keep the 34-row gate blocking; use the 100-row suite as the frozen non-blocking
  comparison dataset for future model/GPU/prompt comparisons.
- Baseline evidence: RunPod A40 `Qwen/Qwen2.5-7B-Instruct` vector run
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z` passed with `90` executed, `1` skipped,
  `0` failures, full-answer transcripts, and `promotion_ready=true`.
- Expanded-suite evidence: RunPod A40 `Qwen/Qwen2.5-14B-Instruct` patched
  `citation-strict-refusal` run `logs/rag_v1_acceptance/cloud/runpod/20260817T165621Z` executed
  all `100` rows, passed `97`, failed `3`, and recorded full-answer transcripts.

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

The active 100-row reviewed suite has this category balance:

- `31` Slurm basics
- `35` Amarel access/storage
- `16` support/software policy
- `10` research-data services
- `8` negative safety
- `0` attachment optional

The reviewed additions cover user-facing procedures and troubleshooting: Slurm scripts, interactive
jobs, arrays, GPU directives, job monitoring, storage quotas, transfer tools, Open OnDemand/FastX,
community software, ownership, license review, research-data service selection, and safety refusals.
The synthetic attachment marker was removed from this benchmark file so future reported comparison
runs have no skipped rows. Attachment tests remain separate.

## Baseline Run

This run is still useful as the original M4 baseline, but it used the previous 91-row benchmark
file with one skipped attachment marker. Rerun the selected 7B baseline on the 100-row suite before
making an apples-to-apples recommendation against newer 100-row runs.

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

## Expanded 100-Row Run

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260817T165621Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260817T165621Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260817T165621Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260817T165621Z/cloud_run_ledger.md`
- Result: `97` pass, `3` fail, `0` skipped, `promotion_ready=false`.
- Failed rows: `amarel_acl_share_file`, `amarel_split_large_box_files`,
  `slurm_maintenance_reservation_check`.
- Manual-review rows: `50` advisory quality-review rows.
- p95 latency: `18023.28` ms.
- p95 time to first token: `948.41` ms.
- Runtime: `1036.958 s`.

## Remaining Runs

Reuse exactly the same 100-row suite for the requested comparisons, with `--full-acceptance`,
`--include-full-answer`, and `--retrieval-mode vector` unless a run explicitly tests retrieval:

- Rerun `Qwen/Qwen2.5-7B-Instruct` on `NVIDIA A40` with patched `citation-strict-refusal` to get a
  clean 100-row reference.
- Triage the three failed rows from the 14B A40 patched-strict run before spending on additional
  14B GPUs.
- `Qwen/Qwen2.5-7B-Instruct` on `NVIDIA GeForce RTX 4090` versus the 100-row A40 reference.
- `Qwen/Qwen2.5-14B-Instruct` on `NVIDIA L40S` and `NVIDIA A100 80GB PCIe` if the A40 14B run is
  promising after failure triage or blocked by memory/performance.
- Prompt variants after adding a recorded selector: `baseline-current`, `citation-strict-refusal`,
  and `concise-procedure`, first on the cheapest clean 7B/GPU baseline.
- `Qwen/Qwen2.5-32B-Instruct` on `NVIDIA A100 80GB PCIe` after the 14B/GPU/prompt baselines.
  Treat L40S/32B as a separate quantization or serving experiment.

No private ServiceNow task JSON, secrets, `.env` files, or raw private corpus should be uploaded for
these runs.
