#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Environment Setup ---
# Define the name for the conda environment.
CONDA_ENV_NAME="oarc-ai-assistant-env"
echo "Conda environment name: $CONDA_ENV_NAME"

# --- Conda Environment ---
# Check if the conda environment already exists.
if conda env list | grep -q "$CONDA_ENV_NAME"; then
    echo "Conda environment '$CONDA_ENV_NAME' already exists."
else
    echo "Creating conda environment '$CONDA_ENV_NAME'..."
    # Create the conda environment with Python 3.10
    conda create -n $CONDA_ENV_NAME python=3.10 -y
fi

# Activate the conda environment.
echo "Activating conda environment '$CONDA_ENV_NAME'..."
conda activate $CONDA_ENV_NAME
conda config --env --set channel_priority strict

# Install mamba if not already installed in the environment
if ! command -v mamba &> /dev/null
then
    echo "Mamba not found, installing mamba..."
    conda install -n $CONDA_ENV_NAME mamba -y
fi

# --- CUDA and Dependencies ---
# Load the appropriate CUDA module for the HPC cluster.
# echo "Loading CUDA module..."
# module load gcc/14.2.0-cermak
# module load cuda/12.1.0
# module load cmake/3.31.8-rdp135

# Install PyTorch, TorchVision, and Sentence-Transformers with Mamba
echo "Installing PyTorch, TorchVision, and Sentence-Transformers with Mamba..."
mamba clean --all

mamba remove -y pytorch libtorch torchvision torchaudio pytorch-cuda torchtriton
mamba install -y --override-channels -c pytorch -c nvidia -c conda-forge \
  pytorch=2.5.1 torchvision=0.20.1 torchaudio=2.5.1 pytorch-cuda=12.1

# Optional (only if you actually need local LLaMA inference)
pip uninstall -y llama-cpp-python
# build from source
sbatch /scratch/ep523/oarc-ai-assistant/env_check/build_llama_cpp.sbatch
# wait

# Install remaining dependencies with pip
echo "Installing remaining Python dependencies from requirements_hpc.txt using pip..."
pip install -r requirements_hpc.txt -c constraints_hpc.txt --upgrade-strategy only-if-needed

# --- Completion ---
echo "Setup complete. The conda environment is ready and dependencies are installed."