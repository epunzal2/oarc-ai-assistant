"""Logging helpers with basic secret redaction for runtime scripts."""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Iterable

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SENSITIVE_ENV_VARS = [
    "HUGGINGFACE_API_TOKEN",
    "VLLM_API_KEY",
    "SGLANG_API_KEY",
    "OPENAI_API_KEY",
]


class RedactingFormatter(logging.Formatter):
    """Formatter that redacts known secret values from log output."""

    def __init__(self, fmt: str, secrets: Iterable[str]):
        super().__init__(fmt)
        self._secrets = [s for s in secrets if s]

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        for secret in self._secrets:
            message = message.replace(secret, "[REDACTED]")
        return message


def _configure_root_logger() -> None:
    secrets = [os.environ.get(var) for var in SENSITIVE_ENV_VARS]
    formatter = RedactingFormatter(LOG_FORMAT, secrets)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10_485_760, backupCount=5)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.INFO)
        root.addHandler(file_handler)
        root.addHandler(stream_handler)
    else:
        # Refresh formatters on existing handlers to ensure redaction applies.
        for handler in root.handlers:
            handler.setFormatter(formatter)


_configure_root_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the specified name.
    """
    return logging.getLogger(name)
