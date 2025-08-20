#!/bin/bash

# This script sets up the environment for Phase 1 deployment on macOS using Homebrew.

# 1. Check for Homebrew and install if we don't have it
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Install llama.cpp using Homebrew
echo "Installing llama.cpp..."
brew install llama.cpp

# 3. Create a directory named models in the project root if it does not already exist
echo "Creating models directory if it doesn't exist..."
mkdir -p models

# 4. Download the Phi-3-mini-4k-instruct-Q4_K_M.gguf model into the models directory
echo "Downloading Phi-3-mini-4k-instruct-Q4_K_M.gguf model..."
wget -O models/phi-3-mini-4k-instruct-q4_k_m.gguf https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4_k_m.gguf

echo "Setup for Phase 1 deployment on macOS is complete."