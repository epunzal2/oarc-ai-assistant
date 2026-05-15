"""Contract tests for repo-local environment setup scripts."""

import re
from pathlib import Path


def test_setup_hpc_uses_uv_sync_and_not_conda() -> None:
    content = Path("scripts/deployment/hpc/setup_hpc.sh").read_text(encoding="utf-8")

    assert "uv sync" in content
    assert ".venv" in content
    assert "conda activate" not in content


def test_setup_local_uses_uv_sync() -> None:
    content = Path("scripts/deployment/macos/setup_local.sh").read_text(encoding="utf-8")

    assert "uv sync" in content
    assert "uv pip install -r requirements.txt" not in content


def test_hpc_requirements_do_not_pin_duplicate_packages() -> None:
    """Keep uv/pip fallback resolution from receiving contradictory pins."""

    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for raw_line in Path("requirements_hpc.txt").read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        package = re.split(r"[<>=!~;\s]", line, maxsplit=1)[0].split("[", maxsplit=1)[0]
        normalized = package.lower().replace("_", "-").replace(".", "-")
        if normalized in seen:
            duplicates.append(f"{normalized}: {seen[normalized]} / {line}")
        seen[normalized] = line

    assert duplicates == []
