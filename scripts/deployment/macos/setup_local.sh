#!/bin/bash

# This script sets up the environment for Phase 1 deployment on macOS using Homebrew.

# 1. Check for Homebrew and install if we don't have it
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Check for uv and exit if it's not installed
echo "Checking for uv..."
if ! command -v uv &> /dev/null; then
    echo "uv not found. Please install it by running: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 3. Create a clean Python virtual environment
echo "Creating a clean Python virtual environment..."
rm -rf .venv
uv venv

# 4. Install dependencies
echo "Installing dependencies from requirements.txt..."
uv pip install -r requirements.txt

# 5. Create a directory named models in the project root if it does not already exist
echo "Creating models directory if it doesn't exist..."
mkdir -p models

# 6. Download the Phi-3-mini-4k-instruct-q4.gguf model into the models directory
echo "Downloading Phi-3-mini-4k-instruct-q4.gguf model..."
huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf Phi-3-mini-4k-instruct-q4.gguf --local-dir models --local-dir-use-symlinks False

echo "Setup is complete. To run the application, follow these steps:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Run in command-line mode: python -m scripts.deployment.macos.chat_local"
echo "3. Or run in web mode: python -m scripts.deployment.macos.chat_local --web"
echo "The chat script locates the model using the LLAMA_CPP_MODEL_PATH variable set in src/rag/config.py."