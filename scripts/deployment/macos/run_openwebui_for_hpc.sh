#!/usr/bin/env bash
#
# Run or prepare a local OpenWebUI client for the verified HPC RAG gateway.
# The GPU Slurm job remains responsible for vLLM and the FastAPI gateway.

set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: run_openwebui_for_hpc.sh --login-host <user@hpc-login> --gateway-compute-host <host> [options]

Validate or start a laptop-to-HPC SSH tunnel, check the tunneled RAG gateway,
and run or print OpenWebUI startup commands for a local demo.

Required:
  --login-host <host>              HPC login host used by ssh, usually user@login-host.
  --gateway-compute-host <host>    Compute node running the RAG gateway.

Options:
  --gateway-port <port>            Gateway port on the compute node (default: 8088).
  --local-gateway-port <port>      Local tunnel port (default: gateway port).
  --openwebui-port <port>          Local OpenWebUI port (default: 3000).
  --mode <docker|native|print>     docker starts OpenWebUI, native prints a native command,
                                   print prints Docker and native commands (default: docker).
  --model <model-id>               Gateway model alias (default: oarc-rag-v1).
  --api-key <key>                  Placeholder gateway key (default: dummy).
  --container-name <name>          Docker container name (default: oarc-rag-openwebui).
  --docker-image <image>           OpenWebUI image (default: ghcr.io/open-webui/open-webui:main).
  --replace-container              Recreate an existing Docker container with the current settings.
  --health-timeout <seconds>       Wait time for the tunneled gateway (default: 30).
  --curl-timeout <seconds>         Per-request curl timeout (default: 10).
  --help                           Show this help message.

Environment defaults:
  HPC_LOGIN_HOST, GATEWAY_COMPUTE_HOST, RAG_GATEWAY_PORT,
  LOCAL_RAG_GATEWAY_PORT, OPENWEBUI_PORT, OPENWEBUI_MODE,
  OPENWEBUI_MODEL, OPENWEBUI_API_KEY, OPENWEBUI_CONTAINER_NAME,
  OPENWEBUI_DOCKER_IMAGE.

OpenWebUI must point at the RAG gateway /v1 endpoint, not raw vLLM.
USAGE
}

die() {
    echo "Error: $*" >&2
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

validate_port() {
    local name="$1"
    local value="$2"

    if [[ ! "${value}" =~ ^[0-9]+$ ]]; then
        die "${name} must be a number: ${value}"
    fi
    if ((10#${value} < 1 || 10#${value} > 65535)); then
        die "${name} must be between 1 and 65535: ${value}"
    fi
}

print_command() {
    printf '  '
    printf '%q ' "$@"
    printf '\n'
}

gateway_health_ok() {
    curl -fsS --max-time "${CURL_TIMEOUT}" "${LOCAL_GATEWAY_URL}/health" >/dev/null
}

wait_for_gateway() {
    local deadline=$((SECONDS + HEALTH_TIMEOUT))

    while ((SECONDS < deadline)); do
        if gateway_health_ok; then
            return 0
        fi
        sleep 2
    done

    return 1
}

ensure_tunnel() {
    local tunnel_spec="127.0.0.1:${LOCAL_GATEWAY_PORT}:${GATEWAY_COMPUTE_HOST}:${GATEWAY_PORT}"
    local foreground_tunnel_spec="${LOCAL_GATEWAY_PORT}:${GATEWAY_COMPUTE_HOST}:${GATEWAY_PORT}"
    local ssh_cmd=(
        ssh
        -f
        -N
        -L "${tunnel_spec}"
        -o ExitOnForwardFailure=yes
        -o ServerAliveInterval=60
        "${LOGIN_HOST}"
    )

    if gateway_health_ok; then
        echo "Existing tunnel is healthy: ${LOCAL_GATEWAY_URL}/health"
        return
    fi

    echo "Starting SSH tunnel to the RAG gateway."
    echo "Foreground equivalent:"
    print_command ssh -N -L "${foreground_tunnel_spec}" "${LOGIN_HOST}"
    "${ssh_cmd[@]}"

    if ! wait_for_gateway; then
        die "tunnel started but ${LOCAL_GATEWAY_URL}/health did not become healthy"
    fi
}

check_gateway() {
    local health_json
    local models_json

    echo
    echo "Checking tunneled RAG gateway:"
    echo "  ${LOCAL_GATEWAY_URL}/health"
    health_json="$(curl -fsS --max-time "${CURL_TIMEOUT}" "${LOCAL_GATEWAY_URL}/health")"
    echo "${health_json}"

    echo
    echo "  ${LOCAL_GATEWAY_URL}/v1/models"
    models_json="$(curl -fsS --max-time "${CURL_TIMEOUT}" "${LOCAL_GATEWAY_URL}/v1/models")"
    echo "${models_json}"

    if ! grep -Fq "${MODEL_ID}" <<<"${models_json}"; then
        die "gateway /v1/models did not include expected model: ${MODEL_ID}"
    fi
}

print_provider_settings() {
    echo
    echo "OpenWebUI provider settings:"
    echo "  Use the RAG gateway, not raw vLLM."
    echo "  Native/local Base URL:       ${NATIVE_PROVIDER_BASE_URL}"
    echo "  Docker Desktop Base URL:    ${DOCKER_PROVIDER_BASE_URL}"
    echo "  Model:                      ${MODEL_ID}"
    echo "  API key:                    ${API_KEY}"
    echo
    echo "Raw vLLM is bypass/debug only. Do not configure OpenWebUI with the raw vLLM /v1 URL."
    echo "If OpenWebUI has existing persisted provider settings, confirm they match these values."
}

print_native_command() {
    echo
    echo "Native OpenWebUI startup command:"
    print_command env \
        OPENAI_API_BASE_URL="${NATIVE_PROVIDER_BASE_URL}" \
        OPENAI_API_KEY="${API_KEY}" \
        python -m open_webui serve --host 127.0.0.1 --port "${OPENWEBUI_PORT}"
}

print_docker_command() {
    echo
    echo "Docker OpenWebUI startup command:"
    print_command docker run -d \
        -p "${OPENWEBUI_PORT}:8080" \
        -v open-webui:/app/backend/data \
        --name "${CONTAINER_NAME}" \
        --restart unless-stopped \
        -e ENABLE_OPENAI_API=True \
        -e OPENAI_API_BASE_URL="${DOCKER_PROVIDER_BASE_URL}" \
        -e OPENAI_API_KEY="${API_KEY}" \
        "${DOCKER_IMAGE}"
}

run_docker_openwebui() {
    local existing_ports

    require_command docker

    print_docker_command

    if docker ps -a --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}"; then
        if [[ "${REPLACE_CONTAINER}" == "true" ]]; then
            echo
            echo "Recreating existing OpenWebUI container: ${CONTAINER_NAME}"
            docker rm -f "${CONTAINER_NAME}" >/dev/null
        else
            echo
            echo "OpenWebUI container already exists: ${CONTAINER_NAME}"
            echo "Starting it if needed. Use --replace-container to recreate it with current settings."
            docker start "${CONTAINER_NAME}" >/dev/null
            existing_ports="$(docker port "${CONTAINER_NAME}" 8080/tcp 2>/dev/null || true)"
            if [[ -n "${existing_ports}" ]]; then
                echo "Existing port mapping: ${existing_ports}"
            fi
            echo "OpenWebUI: http://127.0.0.1:${OPENWEBUI_PORT} if the existing port mapping matches."
            return
        fi
    fi

    echo
    echo "Starting OpenWebUI in Docker Desktop."
    docker run -d \
        -p "${OPENWEBUI_PORT}:8080" \
        -v open-webui:/app/backend/data \
        --name "${CONTAINER_NAME}" \
        --restart unless-stopped \
        -e ENABLE_OPENAI_API=True \
        -e OPENAI_API_BASE_URL="${DOCKER_PROVIDER_BASE_URL}" \
        -e OPENAI_API_KEY="${API_KEY}" \
        "${DOCKER_IMAGE}" >/dev/null

    echo "OpenWebUI: http://127.0.0.1:${OPENWEBUI_PORT}"
}

LOGIN_HOST="${HPC_LOGIN_HOST:-}"
GATEWAY_COMPUTE_HOST="${GATEWAY_COMPUTE_HOST:-}"
GATEWAY_PORT="${RAG_GATEWAY_PORT:-8088}"
LOCAL_GATEWAY_PORT="${LOCAL_RAG_GATEWAY_PORT:-${GATEWAY_PORT}}"
OPENWEBUI_PORT="${OPENWEBUI_PORT:-3000}"
MODE="${OPENWEBUI_MODE:-docker}"
MODEL_ID="${OPENWEBUI_MODEL:-oarc-rag-v1}"
API_KEY="${OPENWEBUI_API_KEY:-dummy}"
CONTAINER_NAME="${OPENWEBUI_CONTAINER_NAME:-oarc-rag-openwebui}"
DOCKER_IMAGE="${OPENWEBUI_DOCKER_IMAGE:-ghcr.io/open-webui/open-webui:main}"
HEALTH_TIMEOUT="${OPENWEBUI_GATEWAY_HEALTH_TIMEOUT:-30}"
CURL_TIMEOUT="${OPENWEBUI_CURL_TIMEOUT:-10}"
REPLACE_CONTAINER="false"

while (($# > 0)); do
    case "$1" in
        --login-host|--hpc-login-host)
            LOGIN_HOST="${2:-}"
            shift 2
            ;;
        --gateway-compute-host|--gateway-host)
            GATEWAY_COMPUTE_HOST="${2:-}"
            shift 2
            ;;
        --gateway-port)
            GATEWAY_PORT="${2:-}"
            shift 2
            ;;
        --local-gateway-port)
            LOCAL_GATEWAY_PORT="${2:-}"
            shift 2
            ;;
        --openwebui-port|--local-openwebui-port)
            OPENWEBUI_PORT="${2:-}"
            shift 2
            ;;
        --mode)
            MODE="${2:-}"
            shift 2
            ;;
        --model)
            MODEL_ID="${2:-}"
            shift 2
            ;;
        --api-key)
            API_KEY="${2:-}"
            shift 2
            ;;
        --container-name)
            CONTAINER_NAME="${2:-}"
            shift 2
            ;;
        --docker-image)
            DOCKER_IMAGE="${2:-}"
            shift 2
            ;;
        --replace-container)
            REPLACE_CONTAINER="true"
            shift
            ;;
        --health-timeout)
            HEALTH_TIMEOUT="${2:-}"
            shift 2
            ;;
        --curl-timeout)
            CURL_TIMEOUT="${2:-}"
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

[[ -n "${LOGIN_HOST}" ]] || die "--login-host is required"
[[ -n "${GATEWAY_COMPUTE_HOST}" ]] || die "--gateway-compute-host is required"

validate_port "--gateway-port" "${GATEWAY_PORT}"
validate_port "--local-gateway-port" "${LOCAL_GATEWAY_PORT}"
validate_port "--openwebui-port" "${OPENWEBUI_PORT}"
validate_port "--health-timeout" "${HEALTH_TIMEOUT}"
validate_port "--curl-timeout" "${CURL_TIMEOUT}"

case "${MODE}" in
    docker|native|print)
        ;;
    *)
        die "--mode must be one of: docker, native, print"
        ;;
esac

require_command ssh
require_command curl

LOCAL_GATEWAY_URL="http://127.0.0.1:${LOCAL_GATEWAY_PORT}"
NATIVE_PROVIDER_BASE_URL="${LOCAL_GATEWAY_URL}/v1"
DOCKER_PROVIDER_BASE_URL="http://host.docker.internal:${LOCAL_GATEWAY_PORT}/v1"

echo "== OpenWebUI for HPC RAG Gateway =="
echo "Login host:          ${LOGIN_HOST}"
echo "Gateway compute:     ${GATEWAY_COMPUTE_HOST}:${GATEWAY_PORT}"
echo "Local gateway:       ${LOCAL_GATEWAY_URL}"
echo "OpenWebUI port:      ${OPENWEBUI_PORT}"
echo "Mode:                ${MODE}"
echo "Gateway model alias: ${MODEL_ID}"
echo
echo "OpenWebUI is a separate UI client. Keep the GPU Slurm job focused on vLLM and the RAG gateway."

ensure_tunnel
check_gateway
print_provider_settings

case "${MODE}" in
    docker)
        run_docker_openwebui
        ;;
    native)
        print_native_command
        echo
        echo "Install native OpenWebUI first if needed: python -m pip install open-webui"
        ;;
    print)
        print_docker_command
        print_native_command
        ;;
esac
