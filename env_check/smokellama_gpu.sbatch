#!/bin/bash
#SBATCH --job-name=smokellama
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint='volta|adalovelace|ampere'
#SBATCH --output=logs/%x_%N_%j.out       # Standard output log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH --error=logs/%x_%N_%j.err        # Standard error log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH -c 2
#SBATCH --mem=16G
#SBATCH -t 00:10:00
set -euo pipefail

module purge
module load gcc/11.2
module load cuda/12.1.0
source "$(conda info --base)/etc/profile.d/conda.sh"
ENVNAME="oarc-ai-rag-test"
echo "conda env: $ENVNAME"
conda activate $ENVNAME

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

# libcuda is present on GPU nodes, so import should work now
python - <<'PY'
import torch, os
print("torch:", torch.__version__, "cuda:", torch.version.cuda, "avail:", torch.cuda.is_available())
from llama_cpp import Llama, __version__ as lver
print("llama-cpp-python:", lver)
# quick offload smoke (adjust path):
# Llama(model_path="models/Phi-3-mini-4k-instruct-q4.gguf", n_gpu_layers=1)
print("Import OK on GPU node")

# faiss-cpu test
import numpy as np, faiss
print("faiss version:", faiss.__version__)
print("FAISS threads:", faiss.omp_get_max_threads())
# make some 2D points
xb = np.array([[0,0],[1,1],[2,2],[3,3]], dtype='float32')
index = faiss.IndexFlatL2(2)  # exact L2 index
index.add(xb)
D, I = index.search(np.array([[0,0]], dtype='float32'), k=2)
print("ntotal:", index.ntotal)
print("neighbors:", I.tolist(), "distances:", D.tolist())
PY


#
