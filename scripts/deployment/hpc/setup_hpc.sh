#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Environment Setup ---
# Define the directory for the virtual environment.
VENV_DIR=".venv"
echo "Virtual environment directory: $VENV_DIR"

# --- Virtual Environment ---
# Check if the virtual environment directory already exists.
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment.
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# --- CUDA and Dependencies ---
# Load the appropriate CUDA module for the HPC cluster.
# This line is a placeholder and may need to be adjusted for your specific cluster.
# Example: module load cuda/11.8
echo "Loading CUDA module (placeholder)..."
# module load cuda/11.8

# Install Python dependencies from requirements.txt.
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Install llama-cpp-python with cuBLAS support.
# The CMAKE_ARGS environment variable is set to enable CUDA support.
# --force-reinstall and --no-cache-dir ensure a clean build.
echo "Installing llama-cpp-python with cuBLAS support..."
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install --force-reinstall --no-cache-dir llama-cpp-python

# --- Completion ---
echo "Setup complete. The virtual environment is ready and dependencies are installed."