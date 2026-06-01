#!/usr/bin/env bash
#
# Check Mac mini host prerequisites without installing anything.

set -euo pipefail

REMOTE="${REMOTE:-mini}"
OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.2:1b}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"

ssh "$REMOTE" "OLLAMA_MODEL='$OLLAMA_MODEL' OLLAMA_BASE_URL='$OLLAMA_BASE_URL' bash -se" <<'REMOTE_SCRIPT'
set -euo pipefail

failures=0

check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "OK: ${label}"
  else
    echo "MISSING: ${label}" >&2
    failures=$((failures + 1))
  fi
}

resolve_ollama() {
  if command -v ollama >/dev/null 2>&1; then
    command -v ollama
  elif [ -x /opt/homebrew/bin/ollama ]; then
    printf '%s\n' /opt/homebrew/bin/ollama
  else
    return 1
  fi
}

check "docker engine" docker info
check "docker compose" docker compose version

if OLLAMA_BIN="$(resolve_ollama)"; then
  echo "OK: ollama CLI (${OLLAMA_BIN})"
else
  cat >&2 <<'EOF'
MISSING: ollama CLI
Install on the Mac mini:
  /opt/homebrew/bin/brew install ollama
Start the service:
  /opt/homebrew/bin/brew services start ollama
EOF
  failures=$((failures + 1))
fi

if curl -fsS "${OLLAMA_BASE_URL}/v1/models" >/dev/null 2>&1; then
  echo "OK: Ollama OpenAI-compatible API at ${OLLAMA_BASE_URL}"
else
  cat >&2 <<EOF
MISSING: Ollama API at ${OLLAMA_BASE_URL}
Start it on the Mac mini:
  OLLAMA_HOST=127.0.0.1:11434 ollama serve
EOF
  failures=$((failures + 1))
fi

if [ -n "${OLLAMA_BIN:-}" ] && "$OLLAMA_BIN" list | awk 'NR > 1 {print $1}' | grep -Fx "$OLLAMA_MODEL" >/dev/null; then
  echo "OK: Ollama model ${OLLAMA_MODEL}"
else
  cat >&2 <<EOF
MISSING: Ollama model ${OLLAMA_MODEL}
Pull it on the Mac mini:
  /opt/homebrew/bin/ollama pull ${OLLAMA_MODEL}
EOF
  failures=$((failures + 1))
fi

echo
docker info --format 'Docker: {{.OSType}}/{{.Architecture}}, CPUs={{.NCPU}}, MemTotal={{.MemTotal}}'
df -h ~

exit "$failures"
REMOTE_SCRIPT
