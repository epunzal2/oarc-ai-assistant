#!/bin/bash

# Slurm Directives for smoke test
#SBATCH --job-name=rag_eval_smoke
#SBATCH --output=logs/%x_%N_%j.out
#SBATCH --error=logs/%x_%N_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint='volta|ampere|adalovelace'
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=00:15:00

set -euo pipefail

mkdir -p logs
PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"
cd "$PROJECT_ROOT"

# Conda environment mirrors env_check/oarc-ai-rag-test.lock.txt
CONDA_ENV_NAME="oarc-ai-rag-test"
source "$(/usr/bin/conda info --base 2>/dev/null || conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

export PYTHONPATH="${SLURM_SUBMIT_DIR:-$PWD}:${PYTHONPATH:-}"
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

# verify model paths
echo "====================================================================================="
echo "Verifying model paths..."
python scripts/models/verify_models.py
echo "====================================================================================="

CONFIG_FILE="configs/evaluation/embedding_bakeoff_smoke.yml"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift
            ;;
        *)
            echo "Unknown parameter passed: $1"
            exit 1
            ;;
    esac
    shift
done

echo "====================================================================================="
echo "Starting smoke evaluation with config: ${CONFIG_FILE}"
echo "====================================================================================="

srun --cpu-bind=cores \
  stdbuf -oL -eL \
  python scripts/evaluation/run_evaluation.py --config "${CONFIG_FILE}"
