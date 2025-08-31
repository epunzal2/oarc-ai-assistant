#!/bin/bash
#SBATCH --job-name=hpc_chat
#SBATCH --output=hpc_chat_%j.out
#SBATCH --error=hpc_chat_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --mem=8G
#SBATCH --time=01:00:00

# Create a logs directory if it doesn't exist
mkdir -p logs

# Activate the virtual environment
source hpc_env/bin/activate

# By default, this script runs the command-line interface and logs to logs/chat_hpc.log
# To run the web server instead, use: python -m scripts.deployment.hpc.chat_hpc --web > logs/chat_hpc_web.log 2>&1
python -m scripts.deployment.hpc.chat_hpc > logs/chat_hpc.log 2>&1