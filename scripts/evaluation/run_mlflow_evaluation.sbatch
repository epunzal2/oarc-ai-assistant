#!/bin/bash

# USAGE: sbatch --export=MLFLOW_TRACKING_URI=http://<hostname>:5000 run_mlflow_evaluation.sbatch

# Slurm Directives
# ----------------
#SBATCH --job-name=mlflow_evaluation
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
echo "IMPORTANT: This script requires a running MLflow tracking server."
echo "You must set the MLFLOW_TRACKING_URI environment variable before submitting this job."
echo
echo "Example:"
echo "  export MLFLOW_TRACKING_URI=http://gpunode-01.hpc.my-university.edu:5000"
echo "  sbatch scripts/evaluation/run_mlflow_evaluation.sbatch"
echo
echo "Current MLFLOW_TRACKING_URI: ${MLFLOW_TRACKING_URI:-'NOT SET. JOB WILL LIKELY FAIL.'}"
echo "====================================================================================="

echo "Registering prompts..."
python scripts/register_prompts.py
echo "Running MLflow evaluation..."

# --- run app (foreground) ---
srun --cpu-bind=cores \
  stdbuf -oL -eL \
  python -m scripts.evaluation.run_mlflow_evaluation \
    --config "configs/evaluation/default.yml" \
    --results "results/batch_run_results.jsonl" \
    --qrels "data/evaluation/gold/qrels.tsv" \
    --output "results/evaluation_metrics.json"

echo "====================================================================================="
echo "Evaluation complete. View the results in the MLflow UI."
echo "If you have an SSH tunnel running, open: http://127.0.0.1:5000"
echo "====================================================================================="