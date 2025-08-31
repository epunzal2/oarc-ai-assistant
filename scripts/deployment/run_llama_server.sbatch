#!/bin/bash
#SBATCH --job-name=llama_server
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=8:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH -p gpu

echo "Running on host: $(hostname)"

./llama.cpp/server -m ./models/mistral-7b-instruct-v0.2.Q5_K_M.gguf --n-gpu-layers 99 --host 0.0.0.0 --port 8080