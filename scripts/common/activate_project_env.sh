#!/usr/bin/env bash

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Source this script from another shell script instead of executing it directly." >&2
    exit 1
fi

PROJECT_ROOT="${PROJECT_ROOT:-$PWD}"
VENV_DIR="${VENV_DIR:-${PROJECT_ROOT}/.venv}"

if [[ ! -f "${VENV_DIR}/bin/activate" ]]; then
    echo "Error: expected virtual environment at ${VENV_DIR}." >&2
    echo "Create it with 'uv sync' (or 'uv sync --extra vllm --extra dev' when needed)." >&2
    return 1
fi

# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

echo "Activated virtual environment: ${VENV_DIR}"
