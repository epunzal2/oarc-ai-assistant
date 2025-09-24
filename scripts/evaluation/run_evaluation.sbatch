#!/bin/bash
#SBATCH --job-name=rag_evaluation
#SBATCH --output=rag_evaluation_%j.out
#SBATCH --error=rag_evaluation_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00

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

# Set up the environment
module load anaconda3
source activate your_conda_env_name # Replace with your conda environment name

# Execute the evaluation script
python scripts/evaluation/run_evaluation.py --config ${CONFIG_FILE}