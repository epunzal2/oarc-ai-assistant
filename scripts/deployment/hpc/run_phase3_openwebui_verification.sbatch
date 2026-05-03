#!/bin/bash
#
# Start vLLM and the FastAPI RAG gateway in one allocation for manual OpenWebUI
# verification. The job prints tunnel instructions and can keep services alive.

# USAGE:
#   sbatch --export=ALL,PROJECT_ROOT=/scratch/$USER/oarc-ai-assistant \
#     scripts/deployment/hpc/run_phase3_openwebui_verification.sbatch
#
# This Phase 3 verification job starts vLLM and the FastAPI RAG gateway in one
# Slurm allocation, runs gateway smoke checks, prints tunnel/OpenWebUI setup
# instructions, and keeps both services alive for manual OpenWebUI testing.

#SBATCH --job-name=phase3_openwebui
#SBATCH --output=logs/%x_%N_%j.out
#SBATCH --error=logs/%x_%N_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint='volta|adalovelace|ampere'
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
cd "${PROJECT_ROOT}"
mkdir -p logs runtime/phase3-openwebui

VLLM_MODEL="${VLLM_MODEL:-meta-llama/Llama-3-8B-Instruct}"
VLLM_HOST="${VLLM_HOST:-0.0.0.0}"
VLLM_PORT="${VLLM_PORT:-8000}"
VLLM_MAX_MODEL_LEN="${VLLM_MAX_MODEL_LEN:-4096}"
VLLM_TENSOR_PARALLEL="${VLLM_TENSOR_PARALLEL:-1}"
VLLM_DTYPE="${VLLM_DTYPE:-auto}"
VLLM_GPU_MEMORY_UTILIZATION="${VLLM_GPU_MEMORY_UTILIZATION:-0.90}"
VLLM_EXTRA_ARGS="${VLLM_EXTRA_ARGS:-}"
VLLM_HEALTH_TIMEOUT="${VLLM_HEALTH_TIMEOUT:-300}"
VLLM_API_KEY="${VLLM_API_KEY:-}"
CUDA_MODULE="${CUDA_MODULE:-cuda/12.1}"

RAG_GATEWAY_HOST="${RAG_GATEWAY_HOST:-0.0.0.0}"
RAG_GATEWAY_PORT="${RAG_GATEWAY_PORT:-8088}"
RAG_GATEWAY_VECTOR_STORE="${RAG_GATEWAY_VECTOR_STORE:-faiss}"
RAG_GATEWAY_LLM_PROVIDER="${RAG_GATEWAY_LLM_PROVIDER:-vllm}"
RAG_GATEWAY_HEALTH_TIMEOUT="${RAG_GATEWAY_HEALTH_TIMEOUT:-300}"
RAG_GATEWAY_PROVIDER_HEALTH_TIMEOUT="${RAG_GATEWAY_PROVIDER_HEALTH_TIMEOUT:-1.0}"
FAISS_INDEX_PATH="${FAISS_INDEX_PATH:-${PROJECT_ROOT}/vector_index/faiss_amarel}"
PHASE3_VERIFY_QUESTION="${PHASE3_VERIFY_QUESTION:-How do I submit a Slurm batch job?}"
PHASE3_KEEPALIVE="${PHASE3_KEEPALIVE:-true}"

if [[ -z "${VLLM_API_KEY}" ]]; then
    VLLM_API_KEY="$(openssl rand -hex 32)"
fi

if command -v module &>/dev/null; then
    echo "Loading module: ${CUDA_MODULE}"
    module load "${CUDA_MODULE}"
fi

source "${PROJECT_ROOT}/scripts/common/activate_project_env.sh"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export VECLIB_MAXIMUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

COMPUTE_HOST="$(hostname -f || hostname)"
VLLM_BASE_URL="http://${COMPUTE_HOST}:${VLLM_PORT}"
VLLM_HEALTH_URL="${VLLM_BASE_URL}/health"
GATEWAY_BASE_URL="http://${COMPUTE_HOST}:${RAG_GATEWAY_PORT}"
GATEWAY_LOCAL_URL="http://127.0.0.1:${RAG_GATEWAY_PORT}"

export VLLM_BASE_URL
export VLLM_HEALTH_URL
export VLLM_MODEL
export VLLM_API_KEY
export RAG_GATEWAY_LLM_PROVIDER
export RAG_GATEWAY_PORT
export RAG_GATEWAY_VECTOR_STORE
export RAG_GATEWAY_PROVIDER_HEALTH_TIMEOUT
export FAISS_INDEX_PATH
export PHASE3_VERIFY_QUESTION

VLLM_PID=""
GATEWAY_PID=""

cleanup() {
    if [[ -n "${GATEWAY_PID}" ]] && kill -0 "${GATEWAY_PID}" 2>/dev/null; then
        kill "${GATEWAY_PID}" 2>/dev/null || true
    fi
    if [[ -n "${VLLM_PID}" ]] && kill -0 "${VLLM_PID}" 2>/dev/null; then
        kill "${VLLM_PID}" 2>/dev/null || true
    fi
}
trap cleanup EXIT

wait_for_http() {
    local name="$1"
    local url="$2"
    local timeout="$3"
    local deadline=$((SECONDS + timeout))
    local http_code="000"

    while [[ ${SECONDS} -lt ${deadline} ]]; do
        http_code="$(curl -s -o /dev/null -w "%{http_code}" "${url}" 2>/dev/null || echo "000")"
        if [[ "${http_code}" != "000" ]] && [[ "${http_code}" -lt 400 ]]; then
            echo "${name} healthy: ${url} (${http_code})"
            return 0
        fi
        sleep 5
    done

    echo "ERROR: ${name} did not become healthy at ${url}; last HTTP code: ${http_code}" >&2
    return 1
}

echo "== Phase 3 OpenWebUI RAG Gateway Verification =="
echo "Project root: ${PROJECT_ROOT}"
echo "Node: ${COMPUTE_HOST}"
echo "Slurm job: ${SLURM_JOB_ID:-N/A}"
echo "vLLM model: ${VLLM_MODEL}"
echo "vLLM base URL: ${VLLM_BASE_URL}"
echo "RAG gateway base URL: ${GATEWAY_BASE_URL}/v1"
echo "RAG vector store: ${RAG_GATEWAY_VECTOR_STORE}"
echo "Verification question: ${PHASE3_VERIFY_QUESTION}"

if [[ "${RAG_GATEWAY_VECTOR_STORE}" == "faiss" && ! -d "${FAISS_INDEX_PATH}" ]]; then
    echo "ERROR: FAISS index directory not found: ${FAISS_INDEX_PATH}" >&2
    exit 1
fi

VLLM_CMD=(
    vllm serve "${VLLM_MODEL}"
    --host "${VLLM_HOST}"
    --port "${VLLM_PORT}"
    --dtype "${VLLM_DTYPE}"
    --max-model-len "${VLLM_MAX_MODEL_LEN}"
    --tensor-parallel-size "${VLLM_TENSOR_PARALLEL}"
    --gpu-memory-utilization "${VLLM_GPU_MEMORY_UTILIZATION}"
    --api-key "${VLLM_API_KEY}"
)

# shellcheck disable=SC2086
if [[ -n "${VLLM_EXTRA_ARGS}" ]]; then
    VLLM_CMD+=(${VLLM_EXTRA_ARGS})
fi

echo "Starting vLLM..."
stdbuf -oL -eL "${VLLM_CMD[@]}" &
VLLM_PID=$!
wait_for_http "vLLM" "${VLLM_HEALTH_URL}" "${VLLM_HEALTH_TIMEOUT}"

cat > "runtime/phase3-openwebui/vllm-endpoint.json" <<ENDPOINT_JSON
{
  "base_url": "${VLLM_BASE_URL}",
  "health_url": "${VLLM_HEALTH_URL}",
  "model": "${VLLM_MODEL}",
  "node": "${COMPUTE_HOST}",
  "port": ${VLLM_PORT},
  "slurm_job_id": "${SLURM_JOB_ID:-}",
  "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "api_key_required": true
}
ENDPOINT_JSON

echo "Starting RAG gateway..."
stdbuf -oL -eL uvicorn src.rag.api:app \
    --host "${RAG_GATEWAY_HOST}" \
    --port "${RAG_GATEWAY_PORT}" &
GATEWAY_PID=$!
wait_for_http "RAG gateway" "${GATEWAY_BASE_URL}/health" "${RAG_GATEWAY_HEALTH_TIMEOUT}"

echo "Running Phase 3 gateway checks..."
python - <<'PY'
import json
import os
import sys
import urllib.request

gateway = f"http://127.0.0.1:{os.environ['RAG_GATEWAY_PORT']}"
question = os.environ["PHASE3_VERIFY_QUESTION"]


def get_json(path: str):
    with urllib.request.urlopen(f"{gateway}{path}", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(path: str, payload: dict):
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{gateway}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.loads(response.read().decode("utf-8"))


health = get_json("/health")
models = get_json("/v1/models")
model_ids = [item.get("id") for item in models.get("data", [])]
if health.get("status") != "ok":
    raise SystemExit(f"/health failed: {health}")
if "oarc-rag-v1" not in model_ids:
    raise SystemExit(f"/v1/models missing oarc-rag-v1: {models}")

completion = post_json(
    "/v1/chat/completions",
    {
        "model": "oarc-rag-v1",
        "messages": [{"role": "user", "content": question}],
    },
)
sources = completion.get("rag_sources") or []
request_id = completion.get("rag_request_id")
answer = completion.get("choices", [{}])[0].get("message", {}).get("content", "")
if not request_id:
    raise SystemExit(f"completion missing rag_request_id: {completion}")
if not sources:
    raise SystemExit(f"completion missing rag_sources: {completion}")

summary = {
    "health_status": health.get("status"),
    "provider_health": health.get("backend", {}).get("provider_health", {}),
    "model_ids": model_ids,
    "rag_request_id": request_id,
    "rag_source_count": len(sources),
    "first_source": sources[0],
    "answer_preview": answer[:500],
}
print(json.dumps(summary, indent=2))
PY

echo
echo "Phase 3 automated checks passed."
echo
echo "OpenWebUI manual verification:"
echo "  1. From your Mac, create an SSH tunnel:"
echo "     ssh -N -L ${RAG_GATEWAY_PORT}:${COMPUTE_HOST}:${RAG_GATEWAY_PORT} <your_hpc_login_host>"
echo
echo "  2. Configure OpenWebUI OpenAI-compatible provider:"
echo "     Base URL: ${GATEWAY_LOCAL_URL}/v1"
echo "     Model:    oarc-rag-v1"
echo "     API key:  any placeholder if OpenWebUI requires one"
echo
echo "  3. Ask this corpus-backed question:"
echo "     ${PHASE3_VERIFY_QUESTION}"
echo
echo "  4. Confirm this job log shows gateway activity and direct API responses include rag_sources."
echo
echo "Raw vLLM is only for bypass/debug:"
echo "  ${VLLM_BASE_URL}/v1"
echo

if [[ "${PHASE3_KEEPALIVE}" == "true" ]]; then
    echo "Keeping vLLM and the RAG gateway alive until Slurm timeout or cancellation."
    wait "${GATEWAY_PID}"
else
    echo "PHASE3_KEEPALIVE=false; stopping services after verification."
fi
