#!/bin/bash

# Slurm Directives
# ----------------
#SBATCH --job-name=rag_chat_hpc                 # Job name
#SBATCH --output=logs/rag_chat_hpc_%j.out       # Standard output log
#SBATCH --error=logs/rag_chat_hpc_%j.err        # Standard error log
#SBATCH --partition=gpu                         # Partition (queue) name
#SBATCH --gres=gpu:1                            # Request one GPU
#SBATCH --cpus-per-task=8                       # Request 8 CPUs per task
#SBATCH --mem=32G                               # Memory allocation
#SBATCH --time=01:00:00                         # Time limit

# Environment Setup
# -----------------
echo "Setting up the environment..."

# Create a logs directory if it doesn't exist
mkdir -p logs

# Load necessary modules (e.g., CUDA)
# module load cuda/11.8  # Adjust the version as per your cluster's configuration

# Activate the Python virtual environment
echo "Activating virtual environment..."
source hpc_env/bin/activate

# Set the number of threads for OpenMP
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Define environment variables for paths and configurations
export MODEL_PATH="/path/to/your/model"  # TODO: Update with the actual model path
export FAISS_INDEX_PATH="faiss_index"
export DB_PATH="vector_store.db"
export DOC_DIR="data/docs"

echo "Environment setup complete."
echo "Running the chat application..."

# Execute the Python script
# -------------------------
# This command runs the chat application with the specified FAISS directory.
# The output will be logged to the files defined by the SBATCH directives.
python -m scripts.deployment.hpc.chat_hpc \
    --faiss_dir "$FAISS_INDEX_PATH" \
    --db_path "$DB_PATH" \
    --doc_dir "$DOC_DIR"

echo "Script execution finished."