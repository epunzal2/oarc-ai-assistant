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
two clean candidate-suite runs, a clean expanded 34-row active gate, and a frozen 91-question
benchmark suite for RunPod model/GPU/config comparisons. Candidate promotion and the 91-question
RunPod A40 baseline are done; the next benchmark work is explicit GPU, prompt, and model variant
comparisons.

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
  candidate fixes, a second clean candidate-suite stability run, candidate promotion, a clean
  expanded 34-row active gate, a reviewed 91-question benchmark suite, and the 91-question RunPod
  A40 baseline are complete. The 4090/A40 cost comparison, Qwen 14B comparison, A100/L40S GPU
  comparison, prompt variants, and roughly 32B-class model trial remain open.
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

### HPC Promotion Preflight

- Attempt date: 2026-08-05.
- Intended login alias: `ep523@amarel-new`.
- Intended project root: `/scratch/ep523/oarc-ai-assistant`.
- Intended model: `Qwen/Qwen2.5-7B-Instruct`, matching the RunPod baseline.
- Intended FAISS path: `/scratch/ep523/oarc-ai-assistant/vector_index/faiss_public`.
- Intended retrieval mode: `vector`, with local-guide fallback enabled.
- Result: blocked before sync. Cisco AnyConnect was installed but disconnected, and local DNS could
  not resolve `amarel.rutgers.edu`, `amarel-new.hpc.rutgers.edu`, or
  `ondemand.hpc.rutgers.edu`.
- Data transfer: none. No repository bundle, FAISS index, ServiceNow data, or secrets were uploaded.

### Benchmark Dataset Expansion

- Raw generated candidate file:
  `data/evaluation/acceptance/rag_v1_candidate_questions.generated.jsonl`
- Reviewed frozen benchmark suite:
  `data/evaluation/acceptance/rag_v1_benchmark_questions.jsonl`
- Raw generation command:
  `.venv/bin/python scripts/evaluation/draft_acceptance_questions.py`
  with approved source roots `docs/google_sites_guide`,
  `docs/slurm-23.02.7/markdown/html`, `docs/slurm-23.02.7/markdown/man`, and
  `docs/corpus/authoritative/rutgers/research-data-finder.md`; max questions `100`; output
  `data/evaluation/acceptance/rag_v1_candidate_questions.generated.jsonl`.
- Raw generated review result: `100` schema-valid rows, no duplicate IDs/questions, no blocked
  `docs/servicenow` paths, but the distribution was unsuitable for a benchmark because `89` rows
  were `slurm_basics` and many late rows were low-value Slurm man-page/admin fragments.
- Reviewed benchmark result: `91` schema-valid rows, no duplicate IDs/questions, no blocked paths.
  Category balance is `30` Slurm basics, `29` Amarel access/storage, `14` support/software policy,
  `9` research-data services, `8` negative safety, and `1` attachment-optional row.
- Decision: keep the 34-question active gate as the blocking smoke/regression suite; use the
  91-question benchmark suite as the fixed non-blocking comparison set across Qwen/Llama/Gemma,
  7B/14B/~32B, A40/4090/A100/L40S, vector/hybrid, prompt variants, and context settings.
- Slurm jobs: none submitted.

### 91-Question RunPod A40 Benchmark Baseline

- Run directory: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z`
- Report: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/report.md`
- Summary: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/summary.json`
- Ledger: `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/cloud_run_ledger.md`
- Plots:
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/plots/latency-by-question.svg`,
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/plots/ttft-by-question.svg`,
  `logs/rag_v1_acceptance/cloud/runpod/20260805T192820Z/plots/source-counts-by-question.svg`
- Questions: `90` executed, `1` skipped synthetic attachment row, `91` total.
- Result: `90` pass, `0` fail, `promotion_ready=true`.
- Manual-review IDs: `39` advisory rows. These are quality-review rows for benchmark analysis,
  not automated gate failures.
- Full answers: included in `results.jsonl`.
- Model: `Qwen/Qwen2.5-7B-Instruct`.
- Retrieval mode: `vector`, with local-guide fallback enabled.
- p50/p95 latency: `3364.42` ms / `10773.45` ms.
- p50/p95 time to first token: `637.2` ms / `861.33` ms.
- Runtime: `601.849 s`.
- Estimated cost: `$0.0718145704` from balance delta.
- Pod: `smckc97h8phopr`, deleted by the runner.
- Cleanup verification: `runpodctl pod list` returned `[]`; `currentSpendPerHr` returned `0`.

Benchmark decision: use this run as the current A40/Qwen2.5-7B/vector baseline for the upcoming
4090/A40, Qwen2.5-14B, A100/L40S, prompt-variant, and roughly 32B-class comparisons. Keep the
34-question active gate as the blocking smoke/regression gate.

Resume checklist after connecting Rutgers VPN with Cisco AnyConnect:

```bash
python3 - <<'PY'
import socket
for host in ("amarel.rutgers.edu", "amarel-new.hpc.rutgers.edu"):
    print(host, socket.getaddrinfo(host, 22)[0][4][0])
PY

ssh -o BatchMode=yes -o ConnectTimeout=10 ep523@amarel-new \
  'hostname -f; whoami; command -v sbatch; command -v uv; pwd'
```

Sync only approved source, public docs, and the public FAISS index. Keep raw ServiceNow exports,
secrets, generated logs, runtime directories, model directories, screenshots, and scratch material
out of the transfer:

```bash
REMOTE=ep523@amarel-new
REMOTE_ROOT=/scratch/ep523/oarc-ai-assistant

ssh "$REMOTE" "mkdir -p '$REMOTE_ROOT'"
rsync -az --info=progress2 \
  --exclude '.git/' \
  --exclude '.env*' \
  --exclude '.venv/' \
  --exclude 'logs/' \
  --exclude 'mlruns/' \
  --exclude 'models/' \
  --exclude 'runtime/' \
  --exclude 'results/' \
  --exclude 'output/' \
  --exclude 'docs/servicenow/' \
  --exclude 'tmp/' \
  --exclude 'scratch/' \
  ./ "$REMOTE:$REMOTE_ROOT/"
```

Then verify the public index and model availability. If an HF-format Qwen model is not already
staged on HPC, stage it first or record the run as a model variant instead of exact RunPod
promotion:

```bash
ssh "$REMOTE" "cd '$REMOTE_ROOT' && ./scripts/deployment/hpc/setup_hpc.sh"
ssh "$REMOTE" "cd '$REMOTE_ROOT' && ls -lh vector_index/faiss_public"
ssh "$REMOTE" \
  "find /scratch/ep523 -maxdepth 7 -type f -name config.json | grep -i 'qwen2.5-7b' || true"
```

Submit the Phase 3 verification job with the RunPod-proven gateway settings:

```bash
ssh "$REMOTE" "cd '$REMOTE_ROOT' && \
  sbatch --partition=gpu-redhat \
    --export=ALL,PROJECT_ROOT='$REMOTE_ROOT',\
VLLM_MODEL='Qwen/Qwen2.5-7B-Instruct',\
FAISS_INDEX_PATH='$REMOTE_ROOT/vector_index/faiss_public',\
SERVICE_NOW_DATA_PATH=/dev/null,\
RAG_GATEWAY_VECTOR_STORE=faiss,\
RAG_GATEWAY_LLM_PROVIDER=vllm,\
RAG_RETRIEVAL_MODE=vector,\
RAG_LOCAL_GUIDE_FALLBACK_ENABLED=true,\
RAG_LOCAL_GUIDE_FALLBACK_TOP_K=12,\
RAG_FINAL_TOP_K=4,\
RAG_MAX_CONTEXT_TOKENS=8192,\
RAG_MAX_CONTEXT_CHARS=12000,\
RAG_UI_ATTACHMENTS_ENABLED=false,\
PHASE3_KEEPALIVE=true \
    scripts/deployment/hpc/run_phase3_openwebui_verification.sbatch"
```

After the Slurm log prints the compute host, open the laptop tunnel and run the active 34-row gate:

```bash
ssh -N -L 8088:<compute-host>:8088 ep523@amarel-new

.venv/bin/python scripts/evaluation/run_v1_acceptance.py \
  --base-url http://127.0.0.1:8088/v1 \
  --output-dir logs/rag_v1_acceptance/hpc/amarel \
  --include-full-answer \
  --max-p95-latency-ms 30000 \
  --max-p95-ttft-ms 15000
```

### Cost Ledger Snapshot

- This Milestone 4 RunPod batch from `20260804T202155Z` through `20260804T213550Z`, including the
  one SSH known-hosts failure ledger, has `13` ledger entries, `2985.943 s` of recorded runtime, and
  `$0.3144250890` estimated ledger cost.
- The 2026-08-05 batch has `7` ledger entries, `2690.36 s` of recorded runtime, and
  `$0.3365055110` estimated ledger cost.
- All RunPod cloud ledgers under `logs/rag_v1_acceptance/cloud/runpod/` currently sum to `23`
  ledger entries, `6277.003 s` of recorded runtime, and `$0.7598457260` estimated ledger cost.
- Latest balance check after billing settled: `$8.8890317482`, `currentSpendPerHr=0`, and
  `runpodctl pod list` returned `[]`.
- One failed setup attempt is recorded at
  `logs/rag_v1_acceptance/cloud/runpod/cloud_run_ledger/oarc-rag-20260804T212403Z/`. It failed
  before transfer because of a recycled RunPod SSH host key, then the runner deleted the pod. The
  code now uses isolated known-hosts files per resource to avoid that failure mode.

## Current Gaps

- The 91-question RunPod A40 baseline is complete; its `39` manual-review rows still need
  qualitative review before using the benchmark as HPC promotion evidence.
- No explicit prompt-variant A/B comparison has been run yet; the earlier batch changed baseline
  prompt cues directly and verified them on RunPod.
- No model-variant comparison has been run yet. The queued order is 4090 versus A40 cost/runtime,
  then Qwen2.5-14B, then A100/L40S comparisons and one roughly 32B-class instruct model.
- Vast remains deferred by current operator decision; no current Vast smoke/full-gate evidence
  exists.
- HPC promotion preflight is blocked until Cisco AnyConnect is connected to Rutgers VPN and Amarel
  DNS resolves from the laptop.

## Next Update

The next report update should be appended after either the 4090/A40 benchmark comparison or Rutgers
VPN reconnection plus HPC sync. Include run directories, comparison artifacts, model/retrieval
settings, GPU type, runtime, cost, Slurm job IDs when applicable, compute host, tunnel port, and
the promotion decision.
