"""Plan/design consistency tests for Phase 5 quality and ops readiness."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "project_docs" / "DESIGN.md"
PHASE_5_PLAN = ROOT / ".plans" / "2026-04-28-phase-5-quality-ops-readiness.md"
GITIGNORE = ROOT / ".gitignore"


def _phase_5_text() -> str:
    design = DESIGN.read_text(encoding="utf-8")
    return design.split("### Phase 5: Quality, Telemetry, and Multi-User Readiness", 1)[
        1
    ].split("### Phase 6:", 1)[0]


def test_phase_5_design_links_plan_and_hpc_gate() -> None:
    phase_5 = _phase_5_text()

    assert ".plans/2026-04-28-phase-5-quality-ops-readiness.md" in phase_5
    assert "Phase 5 planning can begin" in phase_5
    assert "run_phase3_openwebui_verification.sbatch" in phase_5
    assert "HPC-derived settings remain provisional" in phase_5
    assert "project_docs/" in phase_5
    assert ".plans/" in phase_5
    assert "docs/" in phase_5


def test_phase_5_plan_file_exists_and_is_unignored() -> None:
    plan = PHASE_5_PLAN.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")

    assert "Title: Phase 5 Quality, Telemetry, and Multi-User Readiness" in plan
    assert "Status: Draft" in plan
    assert "!/.plans/2026-04-28-phase-5-quality-ops-readiness.md" in gitignore


def test_phase_5_plan_covers_quality_ops_privacy_and_hpc_input_gate() -> None:
    plan = PHASE_5_PLAN.read_text(encoding="utf-8")

    assert "data/evaluation/gold/*" in plan
    assert "MLflow/reporting" in plan
    assert "privacy controls" in plan
    assert "multi-user and load readiness" in plan
    assert "operator workflow" in plan
    assert "HPC Phase 3 verification as the input gate" in plan
    assert "Do not hard-code GPU sizing" in plan
