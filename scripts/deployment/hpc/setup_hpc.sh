#!/bin/bash

# This script sets up the environment for Phase 2 HPC deployment.

# 1. Load the CUDA module
echo "Loading CUDA module..."
module load cuda

# 2. Create a Python virtual environment using uv
echo "Creating Python virtual environment..."
uv venv hpc_env

# 3. Activate the virtual environment
echo "Activating virtual environment..."
source hpc_env/bin/activate

# 4. Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# 5. Reinstall llama-cpp-python with GPU support
echo "Reinstalling llama-cpp-python with CUDA support..."
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install --force-reinstall --no-cache-dir llama-cpp-python

echo "HPC environment setup is complete."