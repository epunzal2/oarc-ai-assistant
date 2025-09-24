#!/bin/bash

# Slurm Directives
# ----------------
#SBATCH --job-name=rag_evaluation                 # Job name
#SBATCH --output=logs/%x_%N_%j.out       # Standard output log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH --error=logs/%x_%N_%j.err        # Standard error log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH --partition=gpu                         # Partition (queue) name
#SBATCH --gres=gpu:1                            # Request one GPU
#SBATCH --constraint='volta|adalovelace|ampere' # V100 32G, L40S 48G, A100 40G
#SBATCH --cpus-per-task=8                       # Request 8 CPUs per task
#SBATCH --mem=32G                               # Memory allocation
#SBATCH --time=01:00:00                         # Time limit

# Environment Setup
# -----------------
set -euo pipefail

# --- basics ---
mkdir -p logs
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"   # set explicitly if you sbatch from elsewhere
cd "$PROJECT_ROOT"

# --- Conda env ---
CONDA_ENV_NAME="oarc-ai-rag-test"
# If 'conda' isn't on PATH, this finds its base
source "$(/usr/bin/conda info --base 2>/dev/null || conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

# --- Python path so 'src/...' imports work when running from project root ---
export PYTHONPATH="${SLURM_SUBMIT_DIR:-$PWD}:${PYTHONPATH:-}"

# --- Threading / misc ---
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

# --- Script arguments ---
# Default configuration file
CONFIG_FILE="configs/evaluation/default.yml"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --config) CONFIG_FILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "====================================================================================="
echo "Starting evaluation with config: ${CONFIG_FILE}"
echo "====================================================================================="

# --- run evaluation ---
srun --cpu-bind=cores \
  stdbuf -oL -eL \
  python scripts/evaluation/run_evaluation.py --config "${CONFIG_FILE}"