from __future__ import annotations

import contextlib
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from src.rag import config
from src.rag.logger import get_logger

logger = get_logger(__name__)

try:  # pragma: no cover - optional dependency
    import mlflow
except Exception:  # pragma: no cover - optional dependency
    mlflow = None


def _mlflow_enabled() -> bool:
    if not config.MLFLOW.enabled:
        return False
    if mlflow is None:
        logger.debug("MLflow unavailable; skipping telemetry.")
        return False
    return True


class _NullRun(contextlib.AbstractContextManager):
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc, tb):
        return False


_experiment_initialized = False


def _ensure_experiment() -> None:
    global _experiment_initialized
    if not _mlflow_enabled():
        return
    if _experiment_initialized:
        return
    try:
        mlflow.set_tracking_uri(config.MLFLOW.tracking_uri)
        mlflow.set_experiment(config.MLFLOW.experiment_name)
        _experiment_initialized = True
    except Exception:
        logger.exception("Failed to initialize MLflow experiment")


def start_run(run_name: str, tags: Optional[Dict[str, Any]] = None, nested: bool = False):
    """Start an MLflow run if enabled, else return a no-op context manager."""
    if not _mlflow_enabled():
        return _NullRun()
    _ensure_experiment()
    try:
        return mlflow.start_run(run_name=run_name, nested=nested, tags=tags or {})
    except Exception:
        logger.exception("Failed to start MLflow run %s", run_name)
        return _NullRun()


def log_params(params: Dict[str, Any]) -> None:
    if not _mlflow_enabled() or not params:
        return
    safe_params = {k: _stringify(v) for k, v in params.items()}
    try:
        mlflow.log_params(safe_params)
    except Exception:
        logger.exception("Failed to log MLflow params")


def log_metrics(metrics: Dict[str, Any], step: Optional[int] = None) -> None:
    if not _mlflow_enabled() or not metrics:
        return
    safe_metrics = {}
    for key, value in metrics.items():
        try:
            safe_metrics[key] = float(value)
        except (TypeError, ValueError):
            continue
    if not safe_metrics:
        return
    try:
        mlflow.log_metrics(safe_metrics, step=step)
    except Exception:
        logger.exception("Failed to log MLflow metrics")


def log_dict(payload: Dict[str, Any], artifact_file: str) -> None:
    if not _mlflow_enabled():
        return
    _log_json_payload(payload, artifact_file)


def log_jsonl(records: Sequence[Dict[str, Any]], artifact_file: str) -> None:
    if not _mlflow_enabled():
        return
    _log_json_payload(list(records), artifact_file, jsonl=True)


def log_text(text: str, artifact_file: str) -> None:
    if not _mlflow_enabled():
        return
    capped = _cap_bytes(text.encode("utf-8"), config.MLFLOW.artifact_max_bytes)
    try:
        mlflow.log_text(capped.decode("utf-8", errors="ignore"), artifact_file)
    except Exception:
        logger.exception("Failed to log text artifact %s", artifact_file)


def log_artifact_from_path(path: Path, artifact_path: Optional[str] = None) -> None:
    if not _mlflow_enabled():
        return
    if not path.exists():
        logger.debug("Artifact path %s missing; skipping", path)
        return
    try:
        mlflow.log_artifact(str(path), artifact_path=artifact_path)
    except Exception:
        logger.exception("Failed to log artifact %s", path)


def hash_text(value: str) -> str:
    if not value:
        return "0000000000000000"
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return digest[:16]


def sanitize_prompt_record(
    record: Dict[str, Any], *, top_k: int, include_answer: bool = True
) -> Dict[str, Any]:
    """Redact prompt text and cap retrieved identifiers."""
    prompt = record.get("question") or record.get("query") or record.get("prompt") or ""
    retrieved = (
        record.get("retrieved_doc_ids")
        or record.get("retrieved_docs")
        or record.get("retrieved_documents")
        or []
    )
    answer = record.get("answer")
    sanitized: Dict[str, Any] = {
        "query_id": record.get("query_id"),
        "prompt_hash": hash_text(prompt),
        "retrieved_doc_ids": list(retrieved)[:max(0, top_k)],
    }
    if include_answer and answer is not None:
        sanitized["answer"] = answer
    if "judge_score" in record:
        sanitized["judge_score"] = record["judge_score"]
    if "llm_judge_score" in record:
        sanitized["llm_judge_score"] = record["llm_judge_score"]
    if "latency_ms" in record:
        sanitized["latency_ms"] = record["latency_ms"]
    if "retrieval_latency_ms" in record:
        sanitized["retrieval_latency_ms"] = record["retrieval_latency_ms"]
    if "ground_truth" in record:
        sanitized["ground_truth"] = record["ground_truth"]
    return sanitized


def sanitize_records(
    records: Iterable[Dict[str, Any]],
    *,
    top_k: int,
    include_answer: bool = True,
) -> List[Dict[str, Any]]:
    return [
        sanitize_prompt_record(record, top_k=top_k, include_answer=include_answer)
        for record in records
    ]


def _log_json_payload(
    payload: Any, artifact_file: str, *, jsonl: bool = False
) -> None:
    bytes_payload: bytes
    if jsonl and isinstance(payload, list):
        lines = "\n".join(json.dumps(item, ensure_ascii=False) for item in payload)
        bytes_payload = lines.encode("utf-8")
    else:
        bytes_payload = json.dumps(payload, ensure_ascii=False, indent=None).encode("utf-8")

    capped = _cap_bytes(bytes_payload, config.MLFLOW.artifact_max_bytes)
    try:
        mlflow.log_text(capped.decode("utf-8", errors="ignore"), artifact_file)
    except Exception:
        logger.exception("Failed to log artifact %s", artifact_file)


def _cap_bytes(payload: bytes, limit: int) -> bytes:
    if len(payload) <= limit:
        return payload
    logger.warning(
        "MLflow artifact exceeds %s bytes (%s); truncating payload",
        limit,
        len(payload),
    )
    return payload[:limit]


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
