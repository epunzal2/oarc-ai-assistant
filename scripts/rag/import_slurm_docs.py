#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.rag.slurm_docs import import_slurm_docs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import the official Slurm source docs into a local RAG-ready corpus.",
    )
    parser.add_argument(
        "--version",
        default="23.02.7",
        help="Slurm version to import.",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/slurm-23.02.7",
        help="Destination directory for the generated corpus.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace the destination directory if it already exists.",
    )
    args = parser.parse_args()

    import_slurm_docs(
        version=args.version,
        output_dir=args.output_dir,
        force=args.force,
    )


if __name__ == "__main__":
    main()
