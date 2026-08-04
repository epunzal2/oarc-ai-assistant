# Cloud RAG Progress Report

This report tracks the OARC RAG chatbot cloud iteration loop as milestones move from RunPod
plumbing into model, retrieval, and answer-quality improvement.

## Current Status

- Date: 2026-08-04
- Current milestone: Milestone 4, benchmark iteration.
- Baseline provider: RunPod.
- Baseline model: `Qwen/Qwen2.5-7B-Instruct` served by `vllm`.
- Baseline retrieval: FAISS, `RAG_RETRIEVAL_MODE=vector`.
- UI surface: assistant-ui React template served by the gateway at `/ui`.
- Current tracked plans:
  - `.plans/2026-07-17-cloud-gpu-rag-iteration.md`
  - `.plans/2026-08-04-assistant-ui-gateway-chat.md`

RunPod baseline parity is complete for the non-attachment gate. The next milestone work is
performance and accuracy iteration: retrieval variants, prompt/model comparisons, candidate-suite
coverage, and repeatable full-gate comparisons.

## Milestone Checklist

- Milestone 0, local and provider prep: mostly done. RunPod auth, SSH, packaging, local public
  FAISS, reports, plots, and ledgers work. Vast CLI/key/SSH remains deferred.
- Milestone 1, one-hour cloud smoke: done on RunPod. RunPod A40 smoke passed and pod cleanup was
  verified. Vast smoke remains deferred.
- Milestone 2, repeatable full acceptance: done on RunPod. Latest full gate passed with no failures
  and no manual-review IDs. Vast full gate remains deferred.
- Milestone 3, RunPod parity: baseline done. Full RunPod gate, live UI screenshot, and assistant-ui
  implementation are done. Attachment-enabled live RunPod screenshot remains pending.
- Milestone 4, benchmark iteration: active now. Compare vector vs hybrid, prompt variants, 7B/8B
  models, candidate suite, and run-to-run stability.
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

## Current Gaps

- RunPod attachment-enabled live screenshot is not done yet.
- No vector-vs-hybrid cloud comparison has been run yet.
- No clean run-to-run comparison report has been generated for the latest full RunPod gate.
- Vast remains deferred; no current Vast smoke/full-gate evidence exists.
- No HPC promotion run has started.

## Next Update

The next report update should be appended after a RunPod attachment-enabled synthetic marker run:

```bash
RUNPOD_API_KEY="$(security find-generic-password -s kx-compute-prices \
  -a RUNPOD_WRITE_API_KEY -w)" \
  .venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
    --provider runpod \
    --runpod-gpu "NVIDIA A40" \
    --execute \
    --enable-ui-attachments \
    --question-id attachment_synthetic_marker \
    --include-full-answer \
    --keep-instance
```

After the screenshot is captured, delete the pod immediately and add the new run directory, ledger,
cost, runtime, screenshot path, and pass/fail result to this report.
