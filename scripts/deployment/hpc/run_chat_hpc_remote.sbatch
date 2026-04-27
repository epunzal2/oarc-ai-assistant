#!/bin/bash

# Slurm Directives
# ----------------
#SBATCH --job-name=rag_chat_hpc_remote
#SBATCH --output=logs/%x_%N_%j.out
#SBATCH --error=logs/%x_%N_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint='volta|adalovelace|ampere'
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00

set -euo pipefail

echo "== Slurm meta =="
echo "Submit dir: ${SLURM_SUBMIT_DIR:-$PWD}"
echo "Node: $(hostname -f)"
echo "JobID: ${SLURM_JOB_ID:-N/A}"

mkdir -p logs
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"
cd "$PROJECT_ROOT"

source "${PROJECT_ROOT}/scripts/common/activate_project_env.sh"

export PYTHONPATH="${SLURM_SUBMIT_DIR:-/scratch/ep523/oarc-ai-assistant}:${PYTHONPATH:-}"
export FAISS_INDEX_PATH="${FAISS_INDEX_PATH:-vector_index/faiss_amarel}"
export EMBEDDING_MODEL="${EMBEDDING_MODEL:-sentence-transformers/all-MiniLM-L6-v2}"
export LLM_PROVIDER="${LLM_PROVIDER:-vllm}"
export PROVIDER_HEALTH_HOST="${PROVIDER_HEALTH_HOST:-127.0.0.1}"
export PROVIDER_HEALTH_TIMEOUT="${PROVIDER_HEALTH_TIMEOUT:-45}"
export PROVIDER_HEALTH_INTERVAL="${PROVIDER_HEALTH_INTERVAL:-5}"
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

PORT="${PORT:-8088}"
HOST="0.0.0.0"
COMPUTE_HOST=$(hostname -f || hostname)

echo "Node: $COMPUTE_HOST"
which python; python -V
echo "LLM provider: ${LLM_PROVIDER}"
if [[ -n "${VLLM_ENDPOINT_DIR:-}" ]]; then
    echo "VLLM endpoint dir: ${VLLM_ENDPOINT_DIR}"
fi
if [[ -n "${VLLM_HEALTH_URL:-}" ]]; then
    echo "VLLM health URL override: ${VLLM_HEALTH_URL}"
fi

if [[ "${LLM_PROVIDER}" == "llama_cpp" ]]; then
    echo "ERR: run_chat_hpc_remote.sbatch is for hosted HTTP providers only." >&2
    echo "Use scripts/deployment/hpc/run_chat_hpc.sbatch for local llama.cpp." >&2
    exit 1
fi

[[ -d "$FAISS_INDEX_PATH" ]] || { echo "ERR: FAISS index dir not found: $FAISS_INDEX_PATH"; exit 1; }

echo "====================================================================================="
echo "Web server will bind on: http://${COMPUTE_HOST}:${PORT}"
echo "From your laptop, create the tunnel via the login node:"
echo
echo "ssh -N -L ${PORT}:${COMPUTE_HOST}:${PORT} your_hpc_username@hpc_login_address"
echo
echo "Then open:  http://127.0.0.1:${PORT}"
echo "Health check (after tunneling): curl -s http://127.0.0.1:${PORT}/health"
echo "====================================================================================="

srun --cpu-bind=cores \
  stdbuf -oL -eL \
  python -m scripts.deployment.hpc.chat_hpc \
    --faiss-dir "$FAISS_INDEX_PATH" \
    --web \
    --host "$HOST" \
    --port "$PORT" \
    --provider "$LLM_PROVIDER" \
    --provider-health-host "$PROVIDER_HEALTH_HOST" \
    --provider-health-timeout "$PROVIDER_HEALTH_TIMEOUT" \
    --provider-health-interval "$PROVIDER_HEALTH_INTERVAL"
