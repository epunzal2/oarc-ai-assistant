#!/bin/bash

# This script sets up the environment for Phase 1 deployment.

# 1. Clone the llama.cpp repository
echo "Cloning llama.cpp repository..."
git clone https://github.com/ggerganov/llama.cpp.git

# 2. Navigate into the newly cloned llama.cpp directory
cd llama.cpp

# 3. Compile the source code with GPU support
echo "Compiling source code with GPU support..."
make LLAMA_CUDA=1

# 4. Navigate back out of the llama.cpp directory
cd ..

# 5. Create a directory named models in the project root if it does not already exist
echo "Creating models directory if it doesn't exist..."
mkdir -p models

# 6. Download the Mistral-7B-Instruct-v0.2.Q5_K_M.gguf model into the models directory
echo "Downloading Mistral-7B-Instruct-v0.2.Q5_K_M.gguf model..."
wget -O models/mistral-7b-instruct-v0.2.Q5_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q5_K_M.gguf

echo "Setup for Phase 1 deployment is complete."