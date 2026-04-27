#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: run_rag_gateway.sh [options]

Start the FastAPI RAG gateway on macOS or another local workstation.

Options:
  --host <host>  Bind host (default: RAG_GATEWAY_HOST or 127.0.0.1)
  --port <port>  Bind port (default: RAG_GATEWAY_PORT or 8088)
  --help         Show this help message

Environment:
  RAG_GATEWAY_LLM_PROVIDER   LLM provider passed to create_rag_chain (default: vllm)
  RAG_GATEWAY_VECTOR_STORE   Vector store passed to create_rag_chain (default: qdrant)
  VLLM_ENDPOINT_DIR          Optional directory used by vLLM config discovery
USAGE
}

HOST="${RAG_GATEWAY_HOST:-127.0.0.1}"
PORT="${RAG_GATEWAY_PORT:-8088}"

while (($# > 0)); do
    case "$1" in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Error: unknown option '$1'." >&2
            usage >&2
            exit 1
            ;;
    esac
done

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)}"
cd "${PROJECT_ROOT}"

source "${PROJECT_ROOT}/scripts/common/activate_project_env.sh"

export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"
export RAG_GATEWAY_LLM_PROVIDER="${RAG_GATEWAY_LLM_PROVIDER:-vllm}"
export RAG_GATEWAY_VECTOR_STORE="${RAG_GATEWAY_VECTOR_STORE:-qdrant}"
export PYTHONUNBUFFERED=1

echo "Starting RAG gateway on http://${HOST}:${PORT}"
echo "Health: http://${HOST}:${PORT}/health"
echo "Models: http://${HOST}:${PORT}/v1/models"

exec uvicorn src.rag.api:app --host "${HOST}" --port "${PORT}"
