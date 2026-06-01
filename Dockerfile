# syntax=docker/dockerfile:1.7

FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:/root/.local/bin:${PATH}"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /usr/local/bin/

COPY pyproject.toml uv.lock README.md LICENSE ./
RUN uv sync --python /usr/local/bin/python3 --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --python /usr/local/bin/python3 --frozen --no-dev

EXPOSE 8088

CMD ["uvicorn", "src.rag.api:app", "--host", "0.0.0.0", "--port", "8088"]
