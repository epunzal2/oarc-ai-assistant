#!/usr/bin/env bash
#
# Deploy the RAG gateway stack to the Mac mini over SSH. The remote `.env` and
# generated runtime artifacts are server-owned and protected from rsync deletes.

set -euo pipefail

APP="${APP:-oarc-rag}"
REMOTE="${REMOTE:-mini}"
REMOTE_DIR="${REMOTE_DIR:-stacks/${APP}}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.macmini.yaml}"
WAIT_TIMEOUT="${WAIT_TIMEOUT:-240}"

RSYNC_FILTERS=(
  --filter='P .env'
  --filter='P runtime/***'
  --filter='P vector_index/***'
  --filter='P logs/***'
  --filter='P mlruns/***'
  --filter='+ docs/'
  --filter='+ docs/google_sites_guide/***'
  --filter='+ docs/slurm-23.02.7/'
  --filter='+ docs/slurm-23.02.7/markdown/***'
  --filter='+ docs/servicenow/'
  --filter='+ docs/servicenow/task_prepared.jsonl'
  --filter='- docs/***'
)

RSYNC_EXCLUDES=(
  --exclude ".git/"
  --exclude ".venv/"
  --exclude "__pycache__/"
  --exclude ".pytest_cache/"
  --exclude ".mypy_cache/"
  --exclude ".ruff_cache/"
  --exclude ".roo/"
  --exclude ".env"
  --exclude ".env.*"
  --exclude "architecture/"
  --exclude "data/"
  --exclude "env_check/"
  --exclude "models/"
  --exclude "project_docs/"
  --exclude "research/"
  --exclude "runtime/"
  --exclude "vector_index/"
  --exclude "logs/"
  --exclude "mlruns/"
  --exclude "results/"
  --exclude "backups/"
  --exclude "scratch/"
  --exclude "tests/"
  --exclude "tmp/"
  --exclude "todo/"
  --exclude "verification/"
  --exclude "*.log"
  --exclude "repo_export.out"
  --exclude "docs/servicenow/task*.json"
)

echo "Deploying ${APP} to ${REMOTE}:${REMOTE_DIR}"

ssh "$REMOTE" "mkdir -p '$REMOTE_DIR'"

rsync -azc --whole-file --delete \
  "${RSYNC_FILTERS[@]}" \
  "${RSYNC_EXCLUDES[@]}" \
  ./ "${REMOTE}:${REMOTE_DIR}/"

ssh "$REMOTE" "APP='$APP' REMOTE_DIR='$REMOTE_DIR' COMPOSE_FILE='$COMPOSE_FILE' WAIT_TIMEOUT='$WAIT_TIMEOUT' bash -se" <<'REMOTE_SCRIPT'
set -euo pipefail

cd "$REMOTE_DIR"

docker info >/dev/null

if [ ! -f ".env" ]; then
  cat >&2 <<EOF
Missing ${REMOTE_DIR}/.env on Mac mini.
Create it once on the Mac mini and keep it server-only:

  ssh mini 'mkdir -p ${REMOTE_DIR} && cat > ${REMOTE_DIR}/.env <<ENV
RAG_GATEWAY_PORT=8088
VLLM_MODEL=llama3.2:1b
MLFLOW_ENABLED=false
TELEMETRY_ENABLED=false
ENV
chmod 600 ${REMOTE_DIR}/.env'
EOF
  exit 2
fi

chmod 600 .env
mkdir -p runtime vector_index logs

docker compose -p "$APP" -f "$COMPOSE_FILE" config >/dev/null
docker compose -p "$APP" -f "$COMPOSE_FILE" pull --ignore-buildable || true
docker compose -p "$APP" -f "$COMPOSE_FILE" up \
  -d \
  --build \
  --remove-orphans \
  --wait \
  --wait-timeout "$WAIT_TIMEOUT" \
  gateway

docker compose -p "$APP" -f "$COMPOSE_FILE" ps
REMOTE_SCRIPT
