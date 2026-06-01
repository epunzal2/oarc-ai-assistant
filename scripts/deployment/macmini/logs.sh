#!/usr/bin/env bash
#
# Follow logs from the Mac mini Compose stack.

set -euo pipefail

APP="${APP:-oarc-rag}"
REMOTE="${REMOTE:-mini}"
REMOTE_DIR="${REMOTE_DIR:-stacks/${APP}}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.macmini.yaml}"
TAIL="${TAIL:-200}"
SERVICE="${1:-}"

ssh "$REMOTE" "APP='$APP' REMOTE_DIR='$REMOTE_DIR' COMPOSE_FILE='$COMPOSE_FILE' TAIL='$TAIL' SERVICE='$SERVICE' bash -se" <<'REMOTE_SCRIPT'
set -euo pipefail

cd "$REMOTE_DIR"

if [ -n "$SERVICE" ]; then
  docker compose -p "$APP" -f "$COMPOSE_FILE" logs --tail "$TAIL" -f "$SERVICE"
else
  docker compose -p "$APP" -f "$COMPOSE_FILE" logs --tail "$TAIL" -f
fi
REMOTE_SCRIPT
