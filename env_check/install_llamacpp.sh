#!/bin/bash

# activate the env that has pip cu121 torch
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate oarc-ai-rag-cu121-pip

# toolchain (no GPU needed to compile)
module load gcc/14.2.0-cermak
module load cuda/12.1.0
module load cmake/3.31.8-rdp135

# make sure the build uses these compilers & CUDA
export CC=$(which gcc)
export CXX=$(which g++)
export CUDACXX=$(which nvcc)
export CUDA_HOME=${CUDA_HOME:-$(dirname $(dirname "$(which nvcc)"))}

# choose the architectures you'll actually use:
# V100(70), A100(80), L40S(89), plus 2080Ti(75) & 3090(86) if you’ll use them.
# ARCHS="70;75;80;86;89"    # drop 75/86 if you don’t need 2080Ti/3090; add 60 for P100
ARCHS="70;80;89"
export CMAKE_ARGS="-DGGML_CUDA=on -DGGML_CUDA_F16=on -DCMAKE_CUDA_ARCHITECTURES=${ARCHS}"
# If you hit “VMM”/memory mapping issues later, rebuild with:
# export CMAKE_ARGS="$CMAKE_ARGS -DGGML_CUDA_NO_VMM=on"

# build from source against your site glibc/CUDA
pip uninstall -y llama-cpp-python
pip install --no-binary=:all: --no-cache-dir --force-reinstall "llama-cpp-python==0.3.16"

# lightweight import test (no GPU needed; just needs CUDA libs)
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH:-}"
python - <<'PY'
from llama_cpp import __version__
print("llama-cpp-python", __version__)
PY

# python - <<'PY'
# import torch
# print("torch:", torch.__version__, "cuda:", torch.version.cuda, "avail:", torch.cuda.is_available())
# if torch.cuda.is_available(): print("device:", torch.cuda.get_device_name(0))
