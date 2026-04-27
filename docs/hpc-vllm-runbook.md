# HPC vLLM Runbook

This runbook covers the hosted vLLM workflow for `oarc-ai-assistant` on the HPC cluster.

## 0. Prepare the HPC virtual environment

```bash
./scripts/deployment/hpc/setup_hpc.sh
source .venv/bin/activate
```

## 1. Choose a shared endpoint directory

```bash
export PROJECT_ROOT="$(pwd)"
export VLLM_ENDPOINT_DIR="${PROJECT_ROOT}/runtime/vllm-endpoints"
mkdir -p "${VLLM_ENDPOINT_DIR}"
```

The serve job publishes `vllm-endpoint.json` here after the endpoint becomes healthy.

## 2. Submit the vLLM serve job

```bash
scripts/deployment/hpc/submit_vllm_serve.sh \
  --model meta-llama/Llama-3-8B-Instruct \
  --endpoint-dir "${VLLM_ENDPOINT_DIR}"
```

Optional overrides:

- `--gpus <count>`
- `--partition <name>`
- `--time <HH:MM:SS>`
- `--port <port>`
- `--api-key <key>`
- `--max-model-len <tokens>`

If `--api-key` is omitted, the submit wrapper generates and prints `VLLM_API_KEY` for the job. Keep
that value in your shell and pass it to later chat jobs with `--export=ALL` so the chat client can
authenticate to vLLM.

## 3. Verify the endpoint

```bash
scripts/deployment/hpc/check_vllm_status.sh --endpoint-dir "${VLLM_ENDPOINT_DIR}"
```

Expected output includes:

- `base_url`
- `health_url`
- `model`
- `slurm_job_id`
- `healthy: true`

## 4. Launch the chat UI against hosted vLLM

```bash
sbatch --export=ALL,LLM_PROVIDER=vllm,VLLM_ENDPOINT_DIR="${VLLM_ENDPOINT_DIR}" \
  scripts/deployment/hpc/run_chat_hpc_remote.sbatch
```

The chat job reads endpoint metadata from `vllm-endpoint.json` unless you explicitly override
`VLLM_BASE_URL`, `VLLM_HEALTH_URL`, or `VLLM_MODEL`.

## 5. Use the app

Create the SSH tunnel printed by the chat job and open the forwarded local URL in your browser.
The app still sends inference requests to:

```text
POST {resolved_base_url}/v1/chat/completions
```

## 6. Stop the shared vLLM server

```bash
scripts/deployment/hpc/stop_vllm_serve.sh --endpoint-dir "${VLLM_ENDPOINT_DIR}"
```

This cancels the SLURM job when possible and removes the published endpoint file.
