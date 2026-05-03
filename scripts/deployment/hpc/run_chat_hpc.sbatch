#!/bin/bash
#
# Launch the legacy Flask/CLI RAG chat harness on one GPU node using a local
# provider and persisted FAISS index. Prefer `run_rag_gateway.sbatch` for the
# OpenAI-compatible gateway path.

# USAGE: sbatch --export=HPC_USER=ep523,LOGIN_HOST=login1.myhpc.edu run_chat.sbatch

# Slurm Directives
# ----------------
#SBATCH --job-name=rag_chat_hpc                 # Job name
#SBATCH --output=logs/%x_%N_%j.out       # Standard output log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH --error=logs/%x_%N_%j.err        # Standard error log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH --partition=gpu                         # Partition (queue) name
#SBATCH --gres=gpu:1                            # Request one GPU
#SBATCH --constraint='volta|adalovelace|ampere' # V100, L40S, A100
#SBATCH --cpus-per-task=8                       # Request 8 CPUs per task
#SBATCH --mem=32G                               # Memory allocation
#SBATCH --time=01:00:00                         # Time limit

# Environment Setup
# -----------------
set -euo pipefail

echo "== Slurm meta =="
echo "Submit dir: ${SLURM_SUBMIT_DIR:-$PWD}"
echo "Node: $(hostname -f)"
echo "JobID: ${SLURM_JOB_ID:-N/A}"

# --- basics ---
mkdir -p logs
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"   # set explicitly if you sbatch from elsewhere
cd "$PROJECT_ROOT"

# --- Repo-local virtual environment ---
source "${PROJECT_ROOT}/scripts/common/activate_project_env.sh"

# --- Python path so 'src/...' imports work when running from project root ---
export PYTHONPATH="${SLURM_SUBMIT_DIR:-/scratch/ep523/oarc-ai-assistant}:${PYTHONPATH:-}"

# --- App configuration ---
export LLAMA_CPP_MODEL_PATH="${LLAMA_CPP_MODEL_PATH:-models/Phi-3-mini-4k-instruct-q4.gguf}"
export FAISS_INDEX_PATH="${FAISS_INDEX_PATH:-vector_index/faiss_amarel}"
PORT="${PORT:-8088}"
export LLM_PROVIDER="${LLM_PROVIDER:-llama_cpp}"
export PROVIDER_HEALTH_HOST="${PROVIDER_HEALTH_HOST:-127.0.0.1}"
export PROVIDER_HEALTH_TIMEOUT="${PROVIDER_HEALTH_TIMEOUT:-45}"
export PROVIDER_HEALTH_INTERVAL="${PROVIDER_HEALTH_INTERVAL:-5}"

# --- Threading / misc ---
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

# --- app config ---
# chat_hpc.py reads model/embedding from src.rag.config; if your config uses env vars, set them here:
export LLAMA_CPP_MODEL_PATH="${LLAMA_CPP_MODEL_PATH:-models/Phi-3-mini-4k-instruct-q4.gguf}"
export EMBEDDING_MODEL="${EMBEDDING_MODEL:-sentence-transformers/all-MiniLM-L6-v2}"

# FAISS index path is passed via CLI
export FAISS_INDEX_PATH="${FAISS_INDEX_PATH:-vector_index/faiss_amarel}"

# Web bind
PORT="${PORT:-8088}"
HOST="0.0.0.0"

# --- sanity info ---
COMPUTE_HOST=$(hostname -f || hostname)
echo "Node: $COMPUTE_HOST"
which python; python -V
nvidia-smi -L || true
python - <<'PY' || true
import torch, faiss
print("torch", torch.__version__, "cuda?", torch.cuda.is_available())
try:
    import llama_cpp
    print("llama_cpp OK")
except Exception as e:
    print("llama_cpp import failed:", e)
print("faiss", faiss.__version__)
try:
    print("faiss threads:", faiss.omp_get_max_threads())
except Exception:
    pass
PY
echo "LLM provider: ${LLM_PROVIDER} (health host: ${PROVIDER_HEALTH_HOST})"

if [[ "${LLM_PROVIDER}" != "llama_cpp" ]]; then
    echo "ERR: run_chat_hpc.sbatch is for local llama.cpp only." >&2
    echo "Use scripts/deployment/hpc/run_chat_hpc_remote.sbatch for hosted HTTP providers such as vLLM." >&2
    exit 1
fi

# --- fail fast on paths ---
[[ -f "$LLAMA_CPP_MODEL_PATH" ]] || { echo "ERR: model not found: $LLAMA_CPP_MODEL_PATH"; exit 1; }
[[ -d "$FAISS_INDEX_PATH"    ]] || { echo "ERR: FAISS index dir not found: $FAISS_INDEX_PATH"; exit 1; }

echo "====================================================================================="
echo "Web server will bind on: http://${COMPUTE_HOST}:${PORT}"
echo "From your laptop, create the tunnel via the login node:"
echo
echo "ssh -N -L ${PORT}:${COMPUTE_HOST}:${PORT} your_hpc_username@hpc_login_address"
echo
echo "Then open:  http://127.0.0.1:${PORT}"
echo "Health check (after tunneling): curl -s http://127.0.0.1:${PORT}/health"
echo "====================================================================================="

# --- run app (foreground) ---
# chat_hpc.py now supports --host/--port
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
