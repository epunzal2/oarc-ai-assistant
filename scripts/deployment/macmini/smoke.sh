#!/usr/bin/env bash
#
# Run an end-to-end smoke request against the Mac mini RAG gateway.

set -euo pipefail

APP="${APP:-oarc-rag}"
REMOTE="${REMOTE:-mini}"
REMOTE_DIR="${REMOTE_DIR:-stacks/${APP}}"
PORT="${RAG_GATEWAY_PORT:-8088}"
QUESTION="${QUESTION:-How do I submit a Slurm job?}"
QUESTION_B64="$(printf '%s' "$QUESTION" | base64 | tr -d '\n')"

ssh "$REMOTE" "REMOTE_DIR='$REMOTE_DIR' PORT='$PORT' QUESTION_B64='$QUESTION_B64' bash -se" <<'REMOTE_SCRIPT'
set -euo pipefail

cd "$REMOTE_DIR"

health="$(curl -fsS "http://127.0.0.1:${PORT}/health")"
models="$(curl -fsS "http://127.0.0.1:${PORT}/v1/models")"
payload="$(
  QUESTION_B64="$QUESTION_B64" python3 - <<'PY'
import base64
import json
import os

question = base64.b64decode(os.environ["QUESTION_B64"]).decode("utf-8")
print(
    json.dumps(
        {
            "model": "oarc-rag-v1",
            "messages": [{"role": "user", "content": question}],
            "stream": False,
        }
    )
)
PY
)"
response="$(
  curl -fsS \
    -H 'Content-Type: application/json' \
    -X POST "http://127.0.0.1:${PORT}/v1/chat/completions" \
    -d "$payload"
)"

HEALTH="$health" MODELS="$models" RESPONSE="$response" python3 - <<'PY'
import json
import os
import sys

health = json.loads(os.environ["HEALTH"])
models = json.loads(os.environ["MODELS"])
response = json.loads(os.environ["RESPONSE"])

provider = health.get("backend", {}).get("provider_health", {})
if provider.get("status") != "ok":
    print(f"Provider health is not ok: {provider}", file=sys.stderr)
    sys.exit(4)

if not models.get("data"):
    print("Gateway returned no models.", file=sys.stderr)
    sys.exit(5)

choices = response.get("choices") or []
if not choices or not choices[0].get("message", {}).get("content"):
    print("Completion response did not include answer content.", file=sys.stderr)
    sys.exit(6)

if not response.get("rag_sources"):
    print("Completion response did not include rag_sources.", file=sys.stderr)
    sys.exit(7)

print("Smoke OK")
print("Request:", response.get("rag_request_id"))
print("Sources:", len(response.get("rag_sources") or []))
print("Answer:", choices[0]["message"]["content"][:500])
PY
REMOTE_SCRIPT
