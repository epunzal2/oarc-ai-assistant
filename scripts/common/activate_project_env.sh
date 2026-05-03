#!/usr/bin/env bash
#
# Shared helper sourced by launch scripts to activate the repo-local virtual
# environment. Inputs: PROJECT_ROOT and VENV_DIR. Side effect: modifies the
# caller shell by sourcing `.venv/bin/activate`.

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
