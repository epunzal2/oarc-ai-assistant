#!/bin/bash

# USAGE: sbatch --export=MLFLOW_TRACKING_URI='http://<hostname>:<port>' run_mlflow_evaluation.sbatch

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
echo "You must provide the server's address (the MLFLOW_TRACKING_URI) for this script to work."
echo
echo "HOW TO FIND THE MLFLOW_TRACKING_URI:"
echo "1. Start the MLflow server using 'sbatch scripts/deployment/hpc/run_mlflow_server.sbatch'."
echo "2. Check the Slurm output file for that job (e.g., 'logs/mlflow_server_...out')."
echo "3. Inside the output file, find the line that says 'MLflow UI is running at:'."
echo "4. The URI is the http address shown, like 'http://gpunode-01.hpc.my-university.edu:5000'."
echo
echo "HOW TO RUN THIS SCRIPT:"
echo "Use the URI you found in the 'sbatch' command like this:"
echo "  sbatch --export=MLFLOW_TRACKING_URI='http://<hostname>:<port>' scripts/evaluation/run_mlflow_evaluation.sbatch"
echo
if [[ -z "${MLFLOW_TRACKING_URI:-}" ]]; then
  echo "ERROR: MLFLOW_TRACKING_URI is not set. Please provide it using --export as shown above."
  exit 1
fi
echo "Using MLFLOW_TRACKING_URI: ${MLFLOW_TRACKING_URI}"
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
echo
echo "HOW TO VIEW THE MLFLOW UI (using an SSH tunnel):"
echo "An SSH tunnel securely connects a port on your local machine to a port on the HPC node."
echo "1. Get the MLflow server's hostname and port from the MLFLOW_TRACKING_URI (e.g., gpunode-01 and 5000)."
echo "2. On your LOCAL machine, run this command:"
echo "   ssh -N -L 5000:<hpc_hostname>:5000 your_username@hpc.cluster.address"
echo "   (Replace <hpc_hostname> with the actual node name, e.g., gpunode-01)."
echo
echo "3. Once the tunnel is active, open this URL in your local web browser:"
echo "   http://127.0.0.1:5000"
echo "====================================================================================="