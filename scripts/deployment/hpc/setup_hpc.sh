#!/bin/bash

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"/../../.. && pwd)}"
VENV_DIR="${VENV_DIR:-${PROJECT_ROOT}/.venv}"
PYTHON_VERSION="${PYTHON_VERSION:-3.10}"

cd "${PROJECT_ROOT}"

if ! command -v uv &> /dev/null; then
    echo "uv not found. Install uv on the HPC environment before running this script." >&2
    exit 1
fi

echo "Project root: ${PROJECT_ROOT}"
echo "Virtual environment: ${VENV_DIR}"
echo "Python version target: ${PYTHON_VERSION}"

if command -v module &> /dev/null; then
    echo "Loading optional compiler/CUDA modules when available..."
    module load cuda/12.1 2>/dev/null || true
fi

echo "Creating or updating repo-local virtual environment with uv..."
uv sync --python "${PYTHON_VERSION}" --extra dev --extra vllm

source "${PROJECT_ROOT}/scripts/common/activate_project_env.sh"

echo "Installing fallback HPC-pinned packages where needed..."
uv pip install -r requirements_hpc.txt -c constraints_hpc.txt --upgrade-strategy only-if-needed

echo "Setup complete. The repo-local virtual environment is ready."
