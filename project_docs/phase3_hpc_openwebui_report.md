# Phase 3 HPC OpenWebUI Verification Report

This report summarizes the Phase 3 proof-of-concept verification for running the OARC RAG
gateway with FAISS retrieval and a local vLLM server. It also separates the completed backend
verification from the remaining UI-client work.

## Status

Phase 3 backend/API verification is complete. Automated checks passed on the `gpu-redhat`
partition on 2026-05-15, and a laptop-to-HPC SSH tunnel successfully reached the live RAG
gateway.

Phase 3b now has a repeatable operator workflow for local UI demos:
`scripts/deployment/macos/run_openwebui_for_hpc.sh`. Live OpenWebUI testing is still pending the
next time the HPC RAG gateway is deployed and tunnelable. That is a client/UI task, not a vLLM or
RAG gateway blocker.

Validated runtime path:

```text
OpenWebUI or another OpenAI-compatible client
  -> RAG gateway OpenAI-compatible endpoint: oarc-rag-v1
  -> FAISS retriever and source-priority post-processing
  -> vLLM OpenAI-compatible endpoint
  -> local Hugging Face-format Llama 3.1 8B Instruct model
```

The successful Slurm job was `54243573` on `gpu022.amarel.rutgers.edu`. The gateway exposed
model ID `oarc-rag-v1`, returned `rag_sources`, and generated an answer for:

```text
How do I submit a Slurm batch job?
```

Tunnel verification from the laptop also passed:

```bash
curl -s http://127.0.0.1:8088/health
curl -s http://127.0.0.1:8088/v1/models
```

Those checks confirmed `vector_store_type=faiss`, backing provider `vllm`, backing model
`/scratch/ep523/deid-local/models/llm/Llama-3.1-8B-Instruct`, and provider health HTTP `200`.

## Working Submission

Use a local Hugging Face-format model directory, not the GGUF model directories under
`models/llm`.

```bash
export PROJECT_ROOT=/scratch/ep523/oarc-ai-assistant
export VLLM_MODEL=/scratch/ep523/deid-local/models/llm/Llama-3.1-8B-Instruct

sbatch --partition=gpu-redhat --export=ALL,PROJECT_ROOT,VLLM_MODEL \
  scripts/deployment/hpc/run_phase3_openwebui_verification.sbatch
```

The current FAISS index used by the successful run was:

```text
/scratch/ep523/oarc-ai-assistant/vector_index/faiss_amarel
```

It was rebuilt from the updated corpus and contained:

```text
index.faiss  23M
index.pkl    20M
```

## UI Integration Scope

The Phase 3 Slurm job does not start OpenWebUI. It starts vLLM and the RAG gateway, then verifies
that the gateway exposes an OpenAI-compatible API. OpenWebUI is one possible UI client for that API.
It must run as a separate self-hosted process on the laptop, a workstation, or another server.

In other words, the backend is already working end to end:

```text
question -> gateway -> FAISS retrieval -> vLLM generation -> answer with sources
```

The UI task is simply:

```text
OpenWebUI -> http://127.0.0.1:8088/v1 -> oarc-rag-v1
```

Keep the Slurm job running, then create a tunnel from the laptop to the gateway process on the
compute node:

```bash
ssh -N -L 8088:gpu022.amarel.rutgers.edu:8088 ep523@amarel-new
```

OpenWebUI should use:

```text
Base URL: http://127.0.0.1:8088/v1
Model:    oarc-rag-v1
API key:  any placeholder if OpenWebUI requires one
```

The tunnel command is expected to produce no output while it is working. Leave that terminal open
and test from another local terminal:

```bash
curl -s http://127.0.0.1:8088/health
curl -s http://127.0.0.1:8088/v1/models
```

Opening `http://127.0.0.1:8088/v1` directly in a browser only reaches the gateway API prefix. It is
not expected to render a chat UI.

For project tracking, Phase 3 should be considered complete for the HPC backend/API path. A
follow-up live UI task should run OpenWebUI through the Phase 3b workflow and save the working
connection settings.

## Phase 3b Operator Workflow

Use the macOS launcher after the HPC Slurm job has started vLLM and the RAG gateway. The script
does not submit GPU work, rebuild FAISS, or start raw vLLM. It only manages the laptop-side tunnel
and OpenWebUI client.

Example:

```bash
scripts/deployment/macos/run_openwebui_for_hpc.sh \
  --login-host ep523@amarel-new \
  --gateway-compute-host gpu022.amarel.rutgers.edu \
  --gateway-port 8088 \
  --local-gateway-port 8088 \
  --openwebui-port 3000 \
  --mode docker
```

The workflow:

1. Reuses an existing healthy tunnel or starts one equivalent to:

   ```bash
   ssh -N -L 8088:gpu022.amarel.rutgers.edu:8088 ep523@amarel-new
   ```

2. Checks the tunneled gateway:

   ```bash
   curl http://127.0.0.1:8088/health
   curl http://127.0.0.1:8088/v1/models
   ```

3. Starts OpenWebUI in Docker mode, or prints exact Docker/native commands in `--mode print` or
   `--mode native`.

4. Prints provider settings:

   ```text
   Native/local Base URL:    http://127.0.0.1:8088/v1
   Docker Desktop Base URL: http://host.docker.internal:8088/v1
   Model:                   oarc-rag-v1
   API key:                 dummy
   ```

OpenWebUI should point to the RAG gateway settings above. Do not point it at the raw vLLM `/v1`
endpoint unless intentionally running a bypass/debug smoke test.

## Issues Found And Resolved

- The original `gpu` partition landed on older nodes without the GLIBC version required by the
  installed PyTorch/vLLM wheels. GPU Slurm scripts now default to `gpu-redhat`.
- `llama-cpp-python` was removed from base dependencies and made optional because production-scale
  vLLM deployments do not need llama.cpp or GGUF compilation.
- The HPC setup script used an unsupported `uv pip install --upgrade-strategy` flag. That flag was
  removed.
- HPC dependency pins had resolver conflicts around `mlflow`, `requests`, `pyarrow`, and the
  PyTorch/vLLM stack. Pins were aligned for the RHEL9/vLLM environment.
- Some HPC nodes did not have `openssl`; vLLM API key generation now uses Python `secrets` with a
  `/dev/urandom` fallback.
- vLLM health checks previously accepted curl `000000`-style failures. Health checks now require
  real 2xx or 3xx HTTP status codes.
- Gated Hugging Face model access blocked `meta-llama/Llama-3-8B-Instruct`. The successful POC used
  an already-staged local HF-format model from `/scratch/ep523/deid-local`.
- Local `models/llm/*` artifacts are GGUF and are not vLLM-compatible. vLLM needs HF-format model
  directories with `config.json`, tokenizer files, and safetensors or bin weights.
- LangChain raised `TypeError: unhashable type: 'SourcePriorityRetriever'` while inspecting the RAG
  runnable graph. The retrieval-policy wrapper now uses identity equality so it remains hashable.

## Non-Blocking Warnings

- vLLM logs `torch_dtype is deprecated`; this is a dependency compatibility warning.
- NCCL logs that `TORCH_NCCL_AVOID_RECORD_STREAMS` is deprecated; this does not block the POC.
- MLflow logs that Git is unavailable in the Slurm job PATH. This only prevents automatic Git SHA
  capture. A production job should either load Git or set `GIT_PYTHON_REFRESH=quiet`.
- vLLM warns that FlashInfer is not installed. It falls back to a PyTorch-native sampler.

## Observations

The deployment path works, but retrieval quality needs attention before treating this as a useful
assistant. The successful answer returned four RAG sources, but the first source for the Slurm
submission question was:

```text
docs/slurm-23.02.7/markdown/html/testimonials.md
```

That is a weak source for a procedural `sbatch` question. This suggests the next retrieval work
should focus on source ranking, document filtering, and Slurm how-to coverage rather than on vLLM
deployment mechanics.

## Recommended Next Steps

1. Hand off to a new Codex session using the checklist in the next section.
2. Run or deploy OpenWebUI through the Phase 3b launcher/workflow and configure it against the
   verified gateway.
3. Capture a few representative prompts from the UI and confirm the gateway logs show
   `rag_sources`.
4. Improve retrieval ranking for common Slurm questions:
   - Prefer `sbatch`, `srun`, `salloc`, and local guide pages over broad or testimonial pages.
   - Consider excluding low-utility Slurm pages such as testimonials from the FAISS corpus.
   - Add regression questions for job submission, GPU allocation, partitions, modules, quotas, and
     scratch/project storage.
5. Decide the model staging strategy for repeat POC and production runs:
   - Direct absolute path to `/scratch/ep523/deid-local/...` for immediate POC.
   - Symlink or documented shared model location for repeatability.
   - Avoid GGUF paths for vLLM jobs.
6. Harden the production deployment path:
   - Stable secret/API-key handling instead of ad hoc generated keys.
   - Explicit endpoint metadata for OpenWebUI and gateway discovery.
   - Cleaner Slurm log separation for vLLM, gateway, and verification probes.
   - Optional `GIT_PYTHON_REFRESH=quiet` or Git module load for MLflow.
7. Keep the FAISS rebuild step tied to corpus changes. Do not rebuild for pure code-only reruns.

## Next Codex Session Handoff

This handoff is a compact state transfer for a future Codex session. It tells the next session what
was proven on HPC, what has already been fixed, what should not be repeated, and which follow-up
phase to pick up next.

Start by reading this report, then inspect `git status --short --untracked-files=all`.

Recent commits in this handoff:

- `34c8a22 fix: keep source-priority retriever hashable`
- `5fc3535 fix: use redhat partition in legacy gpu launcher`

The docs commit that contains this report should be the next commit after those fixes. It tracks:

- `.gitignore`: allows this report to be tracked under `project_docs/`.
- `project_docs/phase3_hpc_openwebui_report.md`: Phase 3 outcome and next-session handoff.
- `project_docs/DESIGN.md`: marks Phase 3 backend/API complete and splits Phase 3b UI setup with
  an operator launcher as the first deliverable.
- `.plans/2026-04-27-openwebui-rag-gateway-integration.md`: marks Phase 3 done and clarifies that
  OpenWebUI installation/configuration is a separate Phase 3b task.

Do not redo the HPC environment work unless the cluster copy is stale. The backend/API path already
passed with Slurm job `54243573`; the laptop tunnel also reached `/health` and `/v1/models`.

If continuing UI work, use the Phase 3b launcher for live UI validation:

```text
run_openwebui_for_hpc.sh -> validate/start the tunnel -> run or instruct OpenWebUI startup
-> select oarc-rag-v1 -> ask corpus-backed questions -> confirm gateway logs and rag_sources.
```

If continuing backend work, prioritize retrieval quality. The deployment path works, but the first
retrieved source for an `sbatch` question was `testimonials.md`, which is not an ideal procedural
source.

Suggested first checks for the next session:

```bash
git status --short --untracked-files=all
git diff --check
python -m compileall -q src/rag/retrieval_policy.py tests/unit/test_retrieval_policy.py
```

Local `pytest` exited with code `-1` and no output in the previous Codex shell. Direct reproduction
checks for the LangChain hashability issue passed, but a normal pytest run should be retried in a
fresh terminal/session.

## Continuation Checklist

- [x] HPC environment installs without llama.cpp build failure.
- [x] FAISS index rebuilt from the updated external corpus.
- [x] vLLM starts on `gpu-redhat` with local HF-format weights.
- [x] RAG gateway starts and loads FAISS.
- [x] Gateway `/health` and `/v1/models` pass.
- [x] Gateway `/v1/chat/completions` passes and returns `rag_sources`.
- [x] Laptop tunnel reaches the live gateway API.
- [x] Phase 3 backend/API path complete.
- [x] Phase 3 outcome and next-session handoff documented.
- [x] Phase 3b operator launcher/workflow implemented.
- [ ] OpenWebUI UI client installed or deployed through that workflow.
- [ ] OpenWebUI configured to use `oarc-rag-v1`.
- [ ] Retrieval quality improved for Slurm operational questions.
- [ ] Production hardening decisions documented.
