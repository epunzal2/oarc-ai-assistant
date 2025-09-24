#!/bin/bash
#SBATCH -p main
#SBATCH --job=llamacpp
#SBATCH --output=%x_%N_%j.out       # Standard output log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH --error=%x_%N_%j.err        # Standard error log (%x=jobname, %N=nodename, %j=jobid)
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 00:30:00
set -euo pipefail

module purge
module load gcc/11.2
module load gcc/11.2/openmpi/4.1.6-ez82
module load cuda/12.1.0
module load cmake/3.31.8-rdp135

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate oarc-ai-rag-cu121-pip
echo "$(which conda)"

export CC=$(which gcc)
export CXX=$(which g++)
export CUDACXX=$(which nvcc)
export CUDA_HOME=${CUDA_HOME:-$(dirname $(dirname "$(which nvcc)"))}
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH:-}"
export CMAKE_BUILD_PARALLEL_LEVEL="${SLURM_CPUS_PER_TASK:-1}"
echo $CMAKE_BUILD_PARALLEL_LEVEL

# target L40S/A100/V100; add ;75;86 if you also use 2080Ti/3090; add ;60 for P100
export CMAKE_ARGS="-DGGML_CUDA=on -DGGML_CUDA_F16=on \
  -DCMAKE_CUDA_ARCHITECTURES=70;80;89 \
  -DCMAKE_CUDA_HOST_COMPILER=${CXX}"
echo $CMAKE_ARGS

pip install --no-binary=llama-cpp-python --no-cache-dir --force-reinstall \
  "llama-cpp-python==0.3.16"

python - <<'PY'
from llama_cpp import __version__
print("llama-cpp-python import OK:", __version__)
PY
