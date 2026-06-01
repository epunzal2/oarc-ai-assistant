#!/usr/bin/env bash
#
# Open a laptop-to-Mac-mini SSH tunnel for the gateway-hosted RAG chat UI.

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/deployment/macmini/ui.sh [--print] [--no-check]

Open an SSH tunnel from the local laptop to the Mac mini RAG gateway and print
the browser URL for the first-party chat UI.

Environment:
  REMOTE            SSH host alias for the Mac mini (default: mini)
  RAG_GATEWAY_PORT  Gateway port on the Mac mini loopback interface (default: 8088)
  LOCAL_UI_PORT     Local browser port for the tunnel (default: 18088)
USAGE
}

REMOTE="${REMOTE:-mini}"
RAG_GATEWAY_PORT="${RAG_GATEWAY_PORT:-8088}"
LOCAL_UI_PORT="${LOCAL_UI_PORT:-18088}"
PRINT_ONLY=false
CHECK_GATEWAY=true

while (($#)); do
  case "$1" in
    --print)
      PRINT_ONLY=true
      ;;
    --no-check)
      CHECK_GATEWAY=false
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

ssh_args=(
  -N
  -L "127.0.0.1:${LOCAL_UI_PORT}:127.0.0.1:${RAG_GATEWAY_PORT}"
  "$REMOTE"
)

print_command() {
  printf 'ssh'
  printf ' %q' "${ssh_args[@]}"
  printf '\n'
}

echo "RAG UI: http://127.0.0.1:${LOCAL_UI_PORT}/ui"
echo "Tunnel:"
print_command

if [[ "$PRINT_ONLY" == "true" ]]; then
  exit 0
fi

if [[ "$CHECK_GATEWAY" == "true" ]]; then
  ssh "$REMOTE" "curl -fsS http://127.0.0.1:${RAG_GATEWAY_PORT}/health >/dev/null"
fi

exec ssh "${ssh_args[@]}"
