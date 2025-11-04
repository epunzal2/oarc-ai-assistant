#!/bin/bash

# USAGE: sbatch run_mlflow_server.sbatch

# Slurm Directives
# ----------------
#SBATCH --job-name=mlflow_server
#SBATCH --output=logs/%x_%N_%j.out
#SBATCH --error=logs/%x_%N_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint='volta|adalovelace|ampere'
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00

# Environment Setup
# -----------------
set -euo pipefail

echo "== Slurm meta =="
echo "Submit dir: ${SLURM_SUBMIT_DIR:-$PWD}"
echo "Node: $(hostname -f)"
echo "JobID: ${SLURM_JOB_ID:-N/A}"

# --- basics ---
mkdir -p logs
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"
cd "$PROJECT_ROOT"

# --- Conda env ---
CONDA_ENV_NAME="oarc-ai-rag-test"
source "$(/usr/bin/conda info --base 2>/dev/null || conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

# --- Python path ---
export PYTHONPATH="${SLURM_SUBMIT_DIR:-/scratch/ep523/oarc-ai-assistant}:${PYTHONPATH:-}"

# --- Threading / misc ---
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

# --- sanity info ---
COMPUTE_HOST=$(hostname -f || hostname)
echo "Node: $COMPUTE_HOST"
which python; python -V

echo "====================================================================================="
echo "MLflow server will bind on: http://${COMPUTE_HOST}:5000"
echo
echo "To access the MLflow dashboard, you need to create an SSH tunnel from your local machine to this compute node."
echo "1. Open a NEW terminal on your LOCAL machine (not on the HPC)."
echo "2. Run the following command in that new terminal:"
echo
echo "   ssh -N -L 5000:${COMPUTE_HOST}:5000 your_hpc_username@hpc_login_address"
echo
echo "   (Replace 'your_hpc_username' and 'hpc_login_address' with your details.)"
echo
echo "3. Once the tunnel is running, open this URL in your local web browser:"
echo "   http://127.0.0.1:5000"
echo
echo "To run experiments, you must set the MLFLOW_TRACKING_URI environment variable."
echo "In the terminal where you will submit your evaluation job, run:"
echo
echo "   export MLFLOW_TRACKING_URI=http://${COMPUTE_HOST}:5000"
echo "====================================================================================="

# --- run app (foreground) ---
srun --cpu-bind=cores \
  stdbuf -oL -eL \
  mlflow server \
    --backend-store-uri sqlite:///mlflow_store/mlflow.db \
    --default-artifact-root ./mlflow_store/artifacts \
    --host 0.0.0.0 \
    --port 5000