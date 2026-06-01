"""Markdown reporting and run comparison for gateway acceptance evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence


def write_acceptance_report(
    run_dir: Path,
    summary: dict[str, Any],
    records: Sequence[dict[str, Any]],
) -> Path:
    """Write `report.md` for one acceptance run and update the summary path."""

    report_path = run_dir / "report.md"
    summary["report_path"] = str(report_path)
    report_path.write_text(render_acceptance_report(summary, records), encoding="utf-8")
    return report_path


def render_acceptance_report(
    summary: dict[str, Any],
    records: Sequence[dict[str, Any]],
) -> str:
    """Render a compact operator-facing Markdown acceptance report."""

    lines = [
        "# Mac mini RAG v1 Acceptance Report",
        "",
        "## Run Metadata",
        "",
        f"- Run directory: `{_value(summary.get('run_dir'))}`",
        f"- Gateway: `{_value(summary.get('base_url'))}`",
        f"- Model alias: `{_value(summary.get('model'))}`",
        f"- Backend model: `{_value(summary.get('backend_model'))}`",
        f"- Vector store: `{_value(summary.get('vector_store_type'))}`",
        f"- Embedding model: `{_value(summary.get('embedding_model'))}`",
        f"- FAISS index path: `{_value(summary.get('faiss_index_path'))}`",
        f"- RAG_RETRIEVAL_MODE: `{_value(summary.get('retrieval_mode'))}`",
        f"- Context tokens: `{_value(summary.get('max_context_tokens'))}`",
        f"- Context chars: `{_value(summary.get('max_context_chars'))}`",
        f"- Attachments enabled: `{summary.get('attachments_enabled')}`",
        f"- Full answers included: `{summary.get('full_answers_included')}`",
        "",
        "## Automated Gates",
        "",
        _metric_line("Questions", summary.get("executed_questions"), summary.get("total_questions")),
        f"- Pass / fail: `{summary.get('pass_count')}` / `{summary.get('fail_count')}`",
        f"- Promotion ready: `{summary.get('promotion_ready')}`",
        f"- p50 / p95 latency ms: `{summary.get('p50_latency_ms')}` / `{summary.get('p95_latency_ms')}`",
        (
            "- p50 / p95 TTFT ms: "
            f"`{summary.get('p50_time_to_first_token_ms')}` / "
            f"`{summary.get('p95_time_to_first_token_ms')}`"
        ),
        (
            "- Positive source count p50 / p95: "
            f"`{summary.get('p50_positive_rag_sources_count')}` / "
            f"`{summary.get('p95_positive_rag_sources_count')}`"
        ),
    ]
    lines.extend(_render_gate_lines(summary.get("automated_gates") or {}))
    lines.extend(
        [
            "",
            "## HPC Promotion Checklist",
            "",
            "| Check | Passed | Note |",
            "| --- | --- | --- |",
        ]
    )
    for key, check in sorted((summary.get("promotion_checklist") or {}).items()):
        if not isinstance(check, dict):
            continue
        lines.append(
            "| "
            f"`{_escape_table(key)}` | "
            f"{_format_bool(check.get('passed'))} | "
            f"{_escape_table(_value(check.get('note')))} |"
        )

    lines.extend(
        [
            "",
            "## Review Queues",
            "",
            f"- Zero-source question IDs: `{', '.join(summary.get('zero_source_question_ids') or [])}`",
            (
                "- Manual-review question IDs: "
                f"`{', '.join(summary.get('manual_review_question_ids') or [])}`"
            ),
            f"- Skipped question IDs: `{', '.join(summary.get('skipped_question_ids') or [])}`",
            "",
            "## Per-Question Evidence",
            "",
            (
                "| ID | Category | Passed | Manual Review | Sources | Latency ms | "
                "TTFT ms | Top Sources | Answer Evidence |"
            ),
            "| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    include_full_answers = bool(summary.get("full_answers_included"))
    for record in records:
        answer = record.get("answer") if include_full_answers else record.get("answer_excerpt")
        lines.append(
            "| "
            f"`{_escape_table(record.get('id'))}` | "
            f"{_escape_table(record.get('category'))} | "
            f"{_format_bool(record.get('passed'))} | "
            f"{_format_bool(record.get('manual_review'))} | "
            f"{record.get('rag_sources_count')} | "
            f"{_value(record.get('latency_ms'))} | "
            f"{_value(record.get('time_to_first_token_ms'))} | "
            f"{_escape_table(_top_sources(record.get('top_sources') or []))} | "
            f"{_escape_table(_truncate(answer, 220))} |"
        )
    lines.append("")
    return "\n".join(lines)


def compare_acceptance_runs(
    run_a: Path | str,
    run_b: Path | str,
    *,
    write_report: bool = True,
) -> dict[str, Any]:
    """Compare two acceptance run directories or summary paths."""

    a_summary, a_records, a_dir = load_run_artifacts(Path(run_a))
    b_summary, b_records, b_dir = load_run_artifacts(Path(run_b))
    comparison = {
        "run_a": _comparison_snapshot(a_summary, a_records),
        "run_b": _comparison_snapshot(b_summary, b_records),
        "deltas": {
            "pass_count": _delta(a_summary, b_summary, "pass_count"),
            "fail_count": _delta(a_summary, b_summary, "fail_count"),
            "p50_latency_ms": _delta(a_summary, b_summary, "p50_latency_ms"),
            "p95_latency_ms": _delta(a_summary, b_summary, "p95_latency_ms"),
            "p50_time_to_first_token_ms": _delta(
                a_summary,
                b_summary,
                "p50_time_to_first_token_ms",
            ),
            "p95_time_to_first_token_ms": _delta(
                a_summary,
                b_summary,
                "p95_time_to_first_token_ms",
            ),
            "p50_positive_rag_sources_count": _delta(
                a_summary,
                b_summary,
                "p50_positive_rag_sources_count",
            ),
            "p95_positive_rag_sources_count": _delta(
                a_summary,
                b_summary,
                "p95_positive_rag_sources_count",
            ),
            "manual_review_count": (
                len(b_summary.get("manual_review_question_ids") or [])
                - len(a_summary.get("manual_review_question_ids") or [])
            ),
        },
        "failed_ids_added": sorted(
            set(_failed_ids(b_records)) - set(_failed_ids(a_records))
        ),
        "failed_ids_removed": sorted(
            set(_failed_ids(a_records)) - set(_failed_ids(b_records))
        ),
        "manual_review_ids_added": sorted(
            set(b_summary.get("manual_review_question_ids") or [])
            - set(a_summary.get("manual_review_question_ids") or [])
        ),
        "manual_review_ids_removed": sorted(
            set(a_summary.get("manual_review_question_ids") or [])
            - set(b_summary.get("manual_review_question_ids") or [])
        ),
    }
    if write_report:
        comparison_path = b_dir / "comparison.md"
        comparison["comparison_path"] = str(comparison_path)
        comparison_path.write_text(render_acceptance_comparison(comparison), encoding="utf-8")
    return comparison


def render_acceptance_comparison(comparison: dict[str, Any]) -> str:
    """Render Markdown for two-run comparison output."""

    run_a = comparison["run_a"]
    run_b = comparison["run_b"]
    deltas = comparison["deltas"]
    lines = [
        "# RAG Acceptance Run Comparison",
        "",
        "| Metric | Run A | Run B | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    metric_keys = (
        "pass_count",
        "fail_count",
        "p50_latency_ms",
        "p95_latency_ms",
        "p50_time_to_first_token_ms",
        "p95_time_to_first_token_ms",
        "p50_positive_rag_sources_count",
        "p95_positive_rag_sources_count",
        "manual_review_count",
    )
    for key in metric_keys:
        lines.append(
            f"| `{key}` | `{_value(run_a.get(key))}` | `{_value(run_b.get(key))}` | "
            f"`{_value(deltas.get(key))}` |"
        )
    lines.extend(
        [
            "",
            "## Run Identity",
            "",
            f"- Run A: `{_value(run_a.get('run_dir'))}` / `{_value(run_a.get('backend_model'))}`",
            f"- Run B: `{_value(run_b.get('run_dir'))}` / `{_value(run_b.get('backend_model'))}`",
            f"- Run A promotion ready: `{run_a.get('promotion_ready')}`",
            f"- Run B promotion ready: `{run_b.get('promotion_ready')}`",
            "",
            "## Question Changes",
            "",
            f"- Failed IDs added: `{', '.join(comparison.get('failed_ids_added') or [])}`",
            f"- Failed IDs removed: `{', '.join(comparison.get('failed_ids_removed') or [])}`",
            (
                "- Manual-review IDs added: "
                f"`{', '.join(comparison.get('manual_review_ids_added') or [])}`"
            ),
            (
                "- Manual-review IDs removed: "
                f"`{', '.join(comparison.get('manual_review_ids_removed') or [])}`"
            ),
            "",
        ]
    )
    return "\n".join(lines)


def load_run_artifacts(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], Path]:
    """Load `summary.json` and `results.jsonl` from a run dir or summary file."""

    summary_path = path if path.name == "summary.json" else path / "summary.json"
    run_dir = summary_path.parent
    results_path = run_dir / "results.jsonl"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in results_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return summary, records, run_dir


def print_comparison(comparison: dict[str, Any]) -> None:
    """Print a compact comparison for CLI usage."""

    print("RAG acceptance comparison")
    print(f"Run A: {comparison['run_a'].get('run_dir')}")
    print(f"Run B: {comparison['run_b'].get('run_dir')}")
    for key, value in comparison["deltas"].items():
        print(f"Delta {key}: {value}")
    if comparison.get("comparison_path"):
        print(f"Comparison report: {comparison['comparison_path']}")


def _comparison_snapshot(summary: dict[str, Any], records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "run_dir": summary.get("run_dir"),
        "backend_model": summary.get("backend_model"),
        "vector_store_type": summary.get("vector_store_type"),
        "retrieval_mode": summary.get("retrieval_mode"),
        "promotion_ready": summary.get("promotion_ready"),
        "pass_count": summary.get("pass_count"),
        "fail_count": summary.get("fail_count"),
        "p50_latency_ms": summary.get("p50_latency_ms"),
        "p95_latency_ms": summary.get("p95_latency_ms"),
        "p50_time_to_first_token_ms": summary.get("p50_time_to_first_token_ms"),
        "p95_time_to_first_token_ms": summary.get("p95_time_to_first_token_ms"),
        "p50_positive_rag_sources_count": summary.get("p50_positive_rag_sources_count"),
        "p95_positive_rag_sources_count": summary.get("p95_positive_rag_sources_count"),
        "manual_review_count": len(summary.get("manual_review_question_ids") or []),
        "failed_question_ids": _failed_ids(records),
        "manual_review_question_ids": summary.get("manual_review_question_ids") or [],
        "automated_gates": summary.get("automated_gates") or {},
    }


def _failed_ids(records: Sequence[dict[str, Any]]) -> list[str]:
    return [
        str(record.get("id"))
        for record in records
        if not record.get("skipped") and not record.get("passed")
    ]


def _delta(run_a: dict[str, Any], run_b: dict[str, Any], key: str) -> float | int | None:
    a_value = run_a.get(key)
    b_value = run_b.get(key)
    if isinstance(a_value, (int, float)) and isinstance(b_value, (int, float)):
        return round(float(b_value) - float(a_value), 2)
    return None


def _render_gate_lines(gates: dict[str, Any]) -> list[str]:
    lines = ["", "| Gate | Passed | Details |", "| --- | --- | --- |"]
    for key, gate in sorted(gates.items()):
        if isinstance(gate, dict):
            details = ", ".join(
                f"{detail_key}={detail_value}"
                for detail_key, detail_value in gate.items()
                if detail_key != "passed"
            )
            passed = gate.get("passed")
        else:
            details = str(gate)
            passed = None
        lines.append(
            f"| `{_escape_table(key)}` | {_format_bool(passed)} | {_escape_table(details)} |"
        )
    return lines


def _metric_line(label: str, numerator: Any, denominator: Any) -> str:
    return f"- {label}: `{_value(numerator)}` / `{_value(denominator)}`"


def _top_sources(sources: Sequence[dict[str, Any]]) -> str:
    rendered = []
    for source in sources:
        title = source.get("title") or source.get("source_title") or source.get("source") or "source"
        path = source.get("source") or source.get("source_path") or source.get("url") or ""
        chunk = source.get("chunk_id") or source.get("id") or ""
        rendered.append(" ".join(str(part) for part in (title, path, chunk) if part))
    return "; ".join(rendered)


def _format_bool(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "n/a"


def _truncate(value: Any, max_chars: int) -> str:
    text = _value(value)
    if len(text) <= max_chars:
        return text
    return f"{text[: max_chars - 3]}..."


def _escape_table(value: Any) -> str:
    return _value(value).replace("|", "\\|").replace("\n", " ")


def _value(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


__all__ = [
    "compare_acceptance_runs",
    "load_run_artifacts",
    "print_comparison",
    "render_acceptance_comparison",
    "render_acceptance_report",
    "write_acceptance_report",
]
