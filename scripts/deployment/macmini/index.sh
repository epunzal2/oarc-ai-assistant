#!/usr/bin/env bash
#
# Build or refresh the Mac-mini-specific FAISS index in a one-shot container.

set -euo pipefail

APP="${APP:-oarc-rag}"
REMOTE="${REMOTE:-mini}"
REMOTE_DIR="${REMOTE_DIR:-stacks/${APP}}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.macmini.yaml}"

ssh "$REMOTE" "APP='$APP' REMOTE_DIR='$REMOTE_DIR' COMPOSE_FILE='$COMPOSE_FILE' bash -se" <<'REMOTE_SCRIPT'
set -euo pipefail

cd "$REMOTE_DIR"

if find docs/servicenow -maxdepth 1 -type f -name 'task*.json' -print -quit 2>/dev/null | grep -q .; then
  echo "Refusing to index: raw ServiceNow task JSON is present on the remote stack." >&2
  exit 3
fi

if [ ! -f "docs/servicenow/task_prepared.jsonl" ]; then
  echo "Missing prepared ServiceNow JSONL: docs/servicenow/task_prepared.jsonl" >&2
  exit 2
fi

mkdir -p runtime vector_index logs
docker compose -p "$APP" -f "$COMPOSE_FILE" run --rm --build indexer
REMOTE_SCRIPT
