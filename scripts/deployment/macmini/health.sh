#!/usr/bin/env bash
#
# Fetch gateway health and model metadata from the Mac mini.

set -euo pipefail

APP="${APP:-oarc-rag}"
REMOTE="${REMOTE:-mini}"
REMOTE_DIR="${REMOTE_DIR:-stacks/${APP}}"
PORT="${RAG_GATEWAY_PORT:-8088}"

ssh "$REMOTE" "REMOTE_DIR='$REMOTE_DIR' PORT='$PORT' bash -se" <<'REMOTE_SCRIPT'
set -euo pipefail

cd "$REMOTE_DIR"

echo "Gateway health:"
curl -fsS "http://127.0.0.1:${PORT}/health"
echo
echo
echo "Gateway models:"
curl -fsS "http://127.0.0.1:${PORT}/v1/models"
echo
REMOTE_SCRIPT
