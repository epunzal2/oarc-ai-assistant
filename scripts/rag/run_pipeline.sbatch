#!/bin/bash

# Slurm Directives
# ----------------
#SBATCH --job-name=run_pipeline_hpc                 # Job name
#SBATCH --output=logs/run_pipeline_hpc_%j.out       # Standard output log
#SBATCH --error=logs/run_pipeline_hpc_%j.err        # Standard error log
#SBATCH --partition=main # Adjust partition name as needed
#SBATCH --cpus-per-task=4                       # Request 4 CPUs per task
#SBATCH --mem=32G                               # Memory allocation
#SBATCH --time=01:00:00                         # Time limit

# Environment Setup
# -----------------
echo "Setting up the environment..."

# Set environment variables to limit CPU usage
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export TOKENIZERS_PARALLELISM=false
echo "OMP_NUM_THREADS:$OMP_NUM_THREADS"

# Load necessary modules (e.g., CUDA)

# Activate the Python virtual environment
echo "Activating virtual environment..."
CONDA_ENV_NAME="oarc-ai-rag-test"
echo "Conda environment name: $CONDA_ENV_NAME"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $CONDA_ENV_NAME

# Execute the pipeline script
# ---------------------------
echo "Starting the RAG pipeline script..."
srun scripts/rag/run_pipeline.sh
echo "Pipeline script finished."