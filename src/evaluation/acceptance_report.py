"""Markdown reporting and run comparison for gateway acceptance evidence."""

from __future__ import annotations

import json
from html import escape
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
    summary["plot_paths"] = write_acceptance_plots(run_dir, records)
    report_path.write_text(render_acceptance_report(summary, records), encoding="utf-8")
    return report_path


def write_acceptance_plots(
    run_dir: Path,
    records: Sequence[dict[str, Any]],
) -> dict[str, str]:
    """Write lightweight SVG plots associated with an acceptance report."""

    plot_dir = run_dir / "plots"
    plots: dict[str, str] = {}
    plot_specs = (
        ("latency_by_question", "latency-by-question.svg", "Latency by Question", "latency_ms", "ms"),
        (
            "ttft_by_question",
            "ttft-by-question.svg",
            "Time to First Token by Question",
            "time_to_first_token_ms",
            "ms",
        ),
        (
            "source_counts_by_question",
            "source-counts-by-question.svg",
            "Source Counts by Question",
            "rag_sources_count",
            "sources",
        ),
    )
    for key, filename, title, value_key, unit in plot_specs:
        points = _plot_points(records, value_key)
        if not points:
            continue
        plot_dir.mkdir(parents=True, exist_ok=True)
        path = plot_dir / filename
        path.write_text(_render_bar_svg(title, points, unit), encoding="utf-8")
        plots[key] = str(path)
    return plots


def render_acceptance_report(
    summary: dict[str, Any],
    records: Sequence[dict[str, Any]],
) -> str:
    """Render a compact operator-facing Markdown acceptance report."""

    lines = [
        "# RAG v1 Acceptance Report",
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
        f"- RAG_PROMPT_VARIANT: `{_value(summary.get('prompt_variant'))}`",
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
    lines.extend(_render_plot_lines(summary.get("plot_paths") or {}))
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


def _plot_points(records: Sequence[dict[str, Any]], value_key: str) -> list[tuple[str, float, bool]]:
    points: list[tuple[str, float, bool]] = []
    for record in records:
        if record.get("skipped"):
            continue
        value = record.get(value_key)
        if not isinstance(value, (int, float)):
            continue
        points.append((str(record.get("id") or "unknown"), float(value), bool(record.get("passed"))))
    return points


def _render_bar_svg(title: str, points: Sequence[tuple[str, float, bool]], unit: str) -> str:
    max_label_chars = 34
    row_height = 24
    top = 44
    bottom = 28
    left = 220
    right = 94
    width = 900
    plot_width = width - left - right
    height = top + bottom + row_height * len(points)
    max_value = max((value for _, value, _ in points), default=1.0) or 1.0
    rows = [
        (
            f'<text x="16" y="26" class="title">{escape(title)}</text>'
            f'<text x="{left}" y="26" class="axis">max {max_value:g} {escape(unit)}</text>'
        )
    ]
    for index, (label, value, passed) in enumerate(points):
        y = top + index * row_height
        bar_width = max(1.0, (value / max_value) * plot_width)
        color = "#2563eb" if passed else "#dc2626"
        label_text = _truncate_middle(label, max_label_chars)
        rows.extend(
            [
                f'<text x="16" y="{y + 14}" class="label">{escape(label_text)}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width:.2f}" height="14" rx="3" fill="{color}" />',
                (
                    f'<text x="{left + bar_width + 8:.2f}" y="{y + 12}" class="value">'
                    f'{value:g} {escape(unit)}</text>'
                ),
            ]
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        'role="img" aria-label="'
        f'{escape(title)}">'
        "<style>"
        "text{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}"
        ".title{font-size:18px;font-weight:700;fill:#111827;}"
        ".axis,.value{font-size:12px;fill:#4b5563;}"
        ".label{font-size:12px;fill:#111827;}"
        "</style>"
        f'<rect width="{width}" height="{height}" fill="#ffffff" />'
        + "".join(rows)
        + "</svg>\n"
    )


def _render_plot_lines(plot_paths: dict[str, Any]) -> list[str]:
    if not plot_paths:
        return []
    plot_specs = (
        ("latency_by_question", "Latency by question", "plots/latency-by-question.svg"),
        ("ttft_by_question", "Time to first token by question", "plots/ttft-by-question.svg"),
        ("source_counts_by_question", "Source counts by question", "plots/source-counts-by-question.svg"),
    )
    lines = ["", "## Plots", ""]
    for key, title, relative_path in plot_specs:
        if plot_paths.get(key):
            lines.extend([f"![{title}]({relative_path})", ""])
    return lines


def _truncate_middle(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    keep = max(1, (limit - 3) // 2)
    return f"{text[:keep]}...{text[-keep:]}"


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
