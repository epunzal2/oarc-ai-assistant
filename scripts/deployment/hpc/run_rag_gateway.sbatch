#!/bin/bash
#
# Start the FastAPI RAG gateway on HPC. Inputs are provided through environment
# variables; side effects are logs plus a long-running uvicorn process.

# USAGE:
#   sbatch --export=ALL,PROJECT_ROOT=/scratch/$USER/oarc-ai-assistant scripts/deployment/hpc/run_rag_gateway.sbatch

#SBATCH --job-name=rag_gateway
#SBATCH --output=logs/%x_%N_%j.out
#SBATCH --error=logs/%x_%N_%j.err
#SBATCH --partition=main
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00

set -euo pipefail

echo "== Slurm meta =="
echo "Submit dir: ${SLURM_SUBMIT_DIR:-$PWD}"
echo "Node: $(hostname -f || hostname)"
echo "JobID: ${SLURM_JOB_ID:-N/A}"

mkdir -p logs
PROJECT_ROOT="${PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}"
cd "${PROJECT_ROOT}"

source "${PROJECT_ROOT}/scripts/common/activate_project_env.sh"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
export RAG_GATEWAY_LLM_PROVIDER="${RAG_GATEWAY_LLM_PROVIDER:-vllm}"
export RAG_GATEWAY_VECTOR_STORE="${RAG_GATEWAY_VECTOR_STORE:-qdrant}"
export RAG_GATEWAY_HOST="${RAG_GATEWAY_HOST:-0.0.0.0}"
export RAG_GATEWAY_PORT="${RAG_GATEWAY_PORT:-8088}"
export RAG_GATEWAY_PROVIDER_HEALTH_TIMEOUT="${RAG_GATEWAY_PROVIDER_HEALTH_TIMEOUT:-1.0}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export VECLIB_MAXIMUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

COMPUTE_HOST="$(hostname -f || hostname)"

echo "RAG gateway provider: ${RAG_GATEWAY_LLM_PROVIDER}"
echo "RAG gateway vector store: ${RAG_GATEWAY_VECTOR_STORE}"
echo "RAG gateway bind: http://${COMPUTE_HOST}:${RAG_GATEWAY_PORT}"
echo "OpenAI-compatible base URL: http://${COMPUTE_HOST}:${RAG_GATEWAY_PORT}/v1"
echo
echo "From your laptop, create a tunnel via the login node:"
echo "ssh -N -L ${RAG_GATEWAY_PORT}:${COMPUTE_HOST}:${RAG_GATEWAY_PORT} your_hpc_username@hpc_login_address"
echo
echo "Then check:"
echo "curl -s http://127.0.0.1:${RAG_GATEWAY_PORT}/health"
echo "curl -s http://127.0.0.1:${RAG_GATEWAY_PORT}/v1/models"

srun --cpu-bind=cores \
  stdbuf -oL -eL \
  uvicorn src.rag.api:app \
    --host "${RAG_GATEWAY_HOST}" \
    --port "${RAG_GATEWAY_PORT}"
