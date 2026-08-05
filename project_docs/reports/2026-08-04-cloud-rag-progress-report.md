# Cloud RAG Progress Report

This report tracks the OARC RAG chatbot cloud iteration loop as milestones move from RunPod
plumbing into model, retrieval, and answer-quality improvement.

## Current Status

- Date: 2026-08-05
- Current milestone: Milestone 4, benchmark iteration.
- Baseline provider: RunPod.
- Baseline model: `Qwen/Qwen2.5-7B-Instruct` served by `vllm`.
- Baseline retrieval: FAISS, `RAG_RETRIEVAL_MODE=vector`, with local-guide fallback from the
  FAISS docstore for selected local-policy questions.
- UI surface: assistant-ui React template served by the gateway at `/ui`.
- Current tracked plans:
  - `.plans/2026-07-17-cloud-gpu-rag-iteration.md`
  - `.plans/2026-08-04-assistant-ui-gateway-chat.md`

RunPod baseline parity is complete, including the attachment-enabled UI path. Milestone 4 now has
two clean candidate-suite runs and a clean expanded 34-row active gate. Candidate promotion is done;
the remaining benchmark work is explicit prompt/model variant comparison, plus HPC promotion when
the chosen cloud configuration is ready to move back to the cluster.

## Milestone Checklist

- Milestone 0, local and provider prep: mostly done. RunPod auth, SSH, packaging, local public
  FAISS, reports, plots, and ledgers work. Vast CLI/key/SSH remains deferred.
- Milestone 1, one-hour cloud smoke: done on RunPod. RunPod A40 smoke passed and pod cleanup was
  verified. Vast smoke remains deferred.
- Milestone 2, repeatable full acceptance: done on RunPod. Latest full gate passed with no failures
  and no manual-review IDs. Vast full gate remains deferred.
- Milestone 3, RunPod parity: done. Full RunPod gate, live UI screenshot, attachment-enabled live UI
  screenshot, and assistant-ui implementation are complete.
- Milestone 4, benchmark iteration: active now. Vector-vs-hybrid, candidate-suite coverage,
  candidate fixes, a second clean candidate-suite stability run, candidate promotion, and a clean
  expanded 34-row active gate are complete on RunPod. Prompt/model variants remain open.
- Milestone 5, HPC promotion: not started. Wait for chosen cloud config plus clean manual review and
  performance evidence.

## Evidence So Far

### Full RunPod Acceptance Gate

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260804T042809Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260804T042809Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260804T042809Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260804T042809Z/cloud_run_ledger.md`
- Questions: `17` executed, `1` skipped synthetic attachment row, `18` total.
- Result: `17` pass, `0` fail, `promotion_ready=true`.
- Manual-review IDs: `[]`.
- p95 latency: `14343.71 ms`.
- p95 time to first token: `347.87 ms`.
- Runtime: `243.478 s`.
- Estimated cost: `$0.0347367630` from balance delta.
- Pod: `v6ozhirn5q5uhl`, deleted by the runner.

The skipped row is the attachment case. It skipped because the gateway was intentionally launched
with attachments disabled before `--enable-ui-attachments` existed.

### Live RunPod UI Smoke

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260804T174931Z`
- Screenshot note:
  `logs/rag_v1_acceptance/cloud/runpod/20260804T174931Z/ui_screenshot_note.md`
- Screenshot artifact:
  `output/playwright/oarc-assistant-ui-runpod-live-desktop.png`
- Question: `How should I request a GPU for a Slurm job?`
- Result: `1` pass, `0` fail, `promotion_ready=true`.
- p95 latency: `2748.96 ms`.
- p95 time to first token: `249.76 ms`.
- Runtime: `165.082 s`.
- Estimated cost: `$0.0506945852` from balance delta.
- Pod: `81w32ac83ayxbl`, manually deleted after screenshot.

This smoke confirmed the browser UI, SSH tunnel, FastAPI gateway, vLLM model, FAISS retrieval,
source inspector, and metadata display were wired together.

### Assistant-UI Implementation

- Commit: `7877031 feat: add assistant-ui rag chat surface`.
- UI source: `src/rag/ui_app/`.
- Served static bundle: `src/rag/ui_static/`.
- Endpoint adapter: same-origin `POST /v1/chat/completions` with OpenAI-style SSE.
- Source and metadata fields preserved:
  `rag_request_id`, `rag_sources`, and public `rag_metadata`.
- Attachments:
  - Default gateway posture remains disabled.
  - Cloud runner now supports `--enable-ui-attachments`.
  - UI includes a generated `sample-attachment.md` action for non-sensitive tests.
- Local attachment screenshot:
  `output/playwright/oarc-assistant-ui-local-attachment-template.png`

### Attachment-Enabled RunPod UI Evidence

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260804T202155Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260804T202155Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260804T202155Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260804T202155Z/cloud_run_ledger.md`
- Screenshot artifact:
  `output/playwright/oarc-assistant-ui-runpod-attachment-live.png`
- Question ID: `attachment_synthetic_marker`.
- Result: `1` pass, `0` fail, `promotion_ready=true`.
- Attachment capability: `attachments_enabled=true`.
- Harness check: `attachment_token_present=true`.
- p95 latency: `1715.99 ms`.
- p95 time to first token: `344.02 ms`.
- Runtime: `207.332 s`.
- Estimated cost: `$0.0253405778` from runtime times pod rate.
- Pod: `xr8i9eeogjlg1w`, manually deleted after screenshot.
- Cleanup verification: `runpodctl pod list` returned `[]`; `currentSpendPerHr` returned `0`.

### Vector Versus Hybrid Benchmark

- Baseline vector run: `logs/rag_v1_acceptance/cloud/runpod/20260804T042809Z`
- Hybrid run: `logs/rag_v1_acceptance/cloud/runpod/20260804T202935Z`
- Comparison report: `logs/rag_v1_acceptance/cloud/runpod/20260804T202935Z/comparison.md`
- Hybrid result: `17` pass, `0` fail, `promotion_ready=true`.
- Hybrid retrieval mode: `hybrid`.
- Hybrid p95 latency: `11817.97 ms`.
- Hybrid p95 time to first token: `630.83 ms`.
- Hybrid manual-review IDs:
  `slurm_check_queue`, `amarel_request_access`, `amarel_storage`, `support_allocations`,
  `support_onboarding`.
- Hybrid runtime: `222.974 s`.
- Hybrid estimated cost: `$0.0158606407` from balance delta.
- Cleanup verification: pod `azq77t3vsrurdq` was deleted; `runpodctl pod list` returned `[]`.

Decision: keep vector as the baseline. Hybrid reduced p95 latency by `2525.74 ms` versus the clean
vector gate, but it increased p95 TTFT by `282.96 ms` and added five manual-review IDs. It should
not be promoted until those answer-quality regressions are fixed.

### Candidate Suite Coverage

- Candidate run: `logs/rag_v1_acceptance/cloud/runpod/20260804T203326Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260804T203326Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260804T203326Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260804T203326Z/cloud_run_ledger.md`
- Result: `14` pass, `2` fail, `promotion_ready=false`.
- Retrieval mode: `vector`.
- p95 latency: `9171.01 ms`.
- p95 time to first token: `553.67 ms`.
- Runtime: `209.781 s`.
- Estimated cost: `$0.0329640519` from balance delta.
- Failed candidate rows: `amarel_login_node_policy`, `slurm_interactive_srun`.
- Manual-review IDs:
  `amarel_access_external_guest_netid`, `amarel_open_ondemand_access`,
  `amarel_scratch_storage_policy`, `slurm_job_array_use_case`,
  `owner_resources_general_vs_owned`.
- Cleanup verification: pod `ax7xebfjk9hwy4` was deleted; `runpodctl pod list` returned `[]`.

Historical decision at this point: hold promotion until the two failing rows and five manual-review
rows were fixed and verified cleanly.

### Candidate Fixes And Current Baseline

Code changes made during Milestone 4:

- Added vector-mode local-guide fallback using the FAISS docstore, so RunPod still transfers only
  the public index bundle rather than raw Markdown corpus or private ServiceNow exports.
- Added targeted prompt cues for external collaborator/Guest NetID access, Open OnDemand,
  `/scratch`, job arrays, owned-vs-general resources, login-node policy, and interactive `srun`.
- Added `RAG_LOCAL_GUIDE_FALLBACK_ENABLED=true` and
  `RAG_LOCAL_GUIDE_FALLBACK_TOP_K=12` defaults, with final context still capped by
  `RAG_FINAL_TOP_K=4`.
- Added isolated per-resource SSH known-hosts files under `runtime/cloud_acceptance/known_hosts/`
  to avoid RunPod recycled IP/port host-key collisions.

Targeted candidate evidence:

- `logs/rag_v1_acceptance/cloud/runpod/20260804T205342Z`: fixed
  `amarel_login_node_policy` and `slurm_interactive_srun`; `2` pass, `0` fail, no manual-review
  IDs.
- `logs/rag_v1_acceptance/cloud/runpod/20260804T211709Z`: fixed
  `amarel_access_external_guest_netid`; `1` pass, `0` fail, no manual-review IDs.

Clean candidate-suite evidence:

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260804T212908Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260804T212908Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260804T212908Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260804T212908Z/cloud_run_ledger.md`
- Result: `16` pass, `0` fail, `promotion_ready=true`.
- Manual-review IDs: `[]`.
- p95 latency: `10210.67 ms`.
- p95 time to first token: `563.49 ms`.
- Runtime: `240.85 s`.
- Estimated cost: `$0.0222879408` from balance delta.
- Pod: `fdpfx8c57lpx00`, deleted by the runner.

Previous 18-question baseline gate:

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260804T213550Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260804T213550Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260804T213550Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260804T213550Z/cloud_run_ledger.md`
- Result: `17` pass, `0` fail, `1` skipped attachment row, `promotion_ready=true`.
- Manual-review IDs: `[]`.
- Zero-source IDs: `safety_password_request`, `safety_raw_ticket_data`.
- p95 latency: `14678.81 ms`.
- p95 time to first token: `637.36 ms`.
- Runtime: `375.238 s`.
- Estimated cost: `$0.0343698519` from balance delta.
- Pod: `f54opmyohbat4c`, deleted by the runner.

Second clean candidate-suite stability run:

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260805T011326Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260805T011326Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260805T011326Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260805T011326Z/cloud_run_ledger.md`
- Result: `16` pass, `0` fail, `promotion_ready=true`.
- Manual-review IDs: `[]`.
- p95 latency: `10338.82 ms`.
- p95 time to first token: `664.53 ms`.
- Runtime: `265.054 s`.
- Estimated cost: `$0.0323954889` from runtime times pod rate.
- Pod: `rzco7hcjn23g79`, deleted by the runner.
- Candidate comparison:
  `logs/rag_v1_acceptance/cloud/runpod/20260805T011326Z/comparison.md`
  versus `logs/rag_v1_acceptance/cloud/runpod/20260804T212908Z`.

Expanded 34-row active gate after candidate promotion:

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/cloud_run_ledger.md`
- Plots:
  `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/plots/latency-by-question.svg`,
  `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/plots/ttft-by-question.svg`,
  `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/plots/source-counts-by-question.svg`
- Result: `33` pass, `0` fail, `1` skipped attachment row, `promotion_ready=true`.
- Manual-review IDs: `[]`.
- Zero-source IDs: `safety_password_request`, `safety_raw_ticket_data`.
- p95 latency: `10594.62 ms`.
- p95 time to first token: `1083.03 ms`.
- Runtime: `360.952 s`.
- Estimated cost: `$0.0741339814` from balance delta.
- Pod: `8lnn3f09cihxvk`, deleted by the runner.
- Expanded-gate comparison:
  `logs/rag_v1_acceptance/cloud/runpod/20260805T012141Z/comparison.md`
  versus `logs/rag_v1_acceptance/cloud/runpod/20260804T213550Z`.

Promotion decision: promote the `16` reviewed candidate rows into
`data/evaluation/acceptance/rag_v1_questions.jsonl`. The promotion gate now has two clean
candidate-suite runs and one clean expanded active-gate run on the current RunPod A40
`Qwen/Qwen2.5-7B-Instruct` vector baseline.

### Cost Ledger Snapshot

- This Milestone 4 RunPod batch from `20260804T202155Z` through `20260804T213550Z`, including the
  one SSH known-hosts failure ledger, has `13` ledger entries, `2985.943 s` of recorded runtime, and
  `$0.3144250890` estimated ledger cost.
- The 2026-08-05 promotion batch has `2` ledger entries, `626.006 s` of recorded runtime, and
  `$0.1065294703` estimated ledger cost.
- All RunPod cloud ledgers under `logs/rag_v1_acceptance/cloud/runpod/` currently sum to `18`
  ledger entries, `4212.649 s` of recorded runtime, and `$0.5298696853` estimated ledger cost.
- Latest balance check after billing settled: `$9.1369140778`, `currentSpendPerHr=0`, and
  `runpodctl pod list` returned `[]`.
- One failed setup attempt is recorded at
  `logs/rag_v1_acceptance/cloud/runpod/cloud_run_ledger/oarc-rag-20260804T212403Z/`. It failed
  before transfer because of a recycled RunPod SSH host key, then the runner deleted the pod. The
  code now uses isolated known-hosts files per resource to avoid that failure mode.

## Current Gaps

- No explicit prompt-variant A/B comparison has been run yet; this batch changed the baseline prompt
  cues directly and verified them on RunPod.
- No model-variant comparison has been run yet.
- Vast remains deferred by current operator decision; no current Vast smoke/full-gate evidence
  exists.
- No HPC promotion run has started.

## Next Update

The next report update should be appended after the first explicit prompt/model variant or the first
HPC promotion attempt. Include run directories, comparison artifacts, cost/runtime ledgers,
model/retrieval settings, and the promotion decision.
