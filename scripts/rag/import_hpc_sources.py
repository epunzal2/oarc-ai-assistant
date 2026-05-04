#!/usr/bin/env python3
"""Dry-run or explicitly import configured optional HPC documentation sources."""

from __future__ import annotations

import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.rag.source_importer import ImportOptions, import_sources


def main() -> None:
    """Parse importer options and write source import reports."""

    parser = argparse.ArgumentParser(
        description="Dry-run or explicitly import Research Pro HPC documentation sources.",
    )
    parser.add_argument(
        "--manifest",
        default="configs/rag_sources/hpc_research_pro_sources.json",
        help="Source manifest config to load.",
    )
    parser.add_argument(
        "--group",
        default="hpc_additional_docs_first_pass",
        help="Configured source group to resolve.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Destination for generated Markdown when --ingest is used.",
    )
    parser.add_argument(
        "--report-dir",
        default=None,
        help="Root directory for import reports.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan and report without fetching pages. This is the default unless --ingest is set.",
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Fetch approved pages and write Markdown output.",
    )
    parser.add_argument(
        "--allow-license-pending",
        action="store_true",
        help="Allow fetching sources whose license/reuse notes still require review.",
    )
    parser.add_argument(
        "--max-pages-per-source",
        type=int,
        default=None,
        help="Cap crawled pages per source.",
    )
    parser.add_argument(
        "--ignore-robots",
        action="store_true",
        help="Do not check robots.txt. Use only for local fixtures or reviewed mirrors.",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional stable report run id.",
    )
    args = parser.parse_args()

    dry_run = args.dry_run or not args.ingest
    report = import_sources(
        ImportOptions(
            manifest_path=args.manifest,
            group=args.group,
            output_dir=args.output_dir,
            report_dir=args.report_dir,
            ingest=args.ingest,
            dry_run=dry_run,
            allow_license_pending=args.allow_license_pending,
            max_pages_per_source=args.max_pages_per_source,
            obey_robots_txt=not args.ignore_robots,
            run_id=args.run_id,
        )
    )
    print(f"Report written to {report.summary['report_dir']}")
    print(
        "sources_imported={sources_imported} sources_skipped={sources_skipped} "
        "crawl_errors={crawl_errors}".format(**report.summary)
    )


if __name__ == "__main__":
    main()
