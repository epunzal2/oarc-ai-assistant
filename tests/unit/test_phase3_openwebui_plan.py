from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "project_docs" / "DESIGN.md"
PHASE_1_PLAN = ROOT / ".plans" / "2026-04-27-rag-openai-api-boundary.md"
PHASE_2_PLAN = ROOT / ".plans" / "2026-04-27-rag-streaming-source-metadata.md"
PHASE_3_PLAN = ROOT / ".plans" / "2026-04-27-openwebui-rag-gateway-integration.md"
GITIGNORE = ROOT / ".gitignore"


def _phase_text(phase_header: str, next_phase_header: str) -> str:
    design = DESIGN.read_text(encoding="utf-8")
    return design.split(phase_header, 1)[1].split(next_phase_header, 1)[0]


def test_phase_1_design_and_plan_mark_api_boundary_done() -> None:
    phase_1 = _phase_text("### Phase 1: RAG-Compatible API Boundary", "### Phase 2:")
    plan = PHASE_1_PLAN.read_text(encoding="utf-8")

    assert "- [ ]" not in phase_1
    assert ".plans/2026-04-27-rag-openai-api-boundary.md" in phase_1
    assert "src/rag/api.py" in phase_1
    assert "tests/unit/test_rag_gateway.py" in phase_1
    assert "Status: Done" in plan
    assert "GET /health" in plan
    assert "POST /v1/chat/completions" in plan


def test_phase_2_design_and_plan_mark_streaming_sources_done() -> None:
    phase_2 = _phase_text("### Phase 2: Streaming and Source Metadata", "### Phase 3:")
    plan = PHASE_2_PLAN.read_text(encoding="utf-8")

    assert "- [ ]" not in phase_2
    assert ".plans/2026-04-27-rag-streaming-source-metadata.md" in phase_2
    assert "src/rag/rag_pipeline.py" in phase_2
    assert "Status: Done" in plan
    assert "rag_sources" in plan
    assert "stream: true" in plan


def test_phase_3_design_links_plan_and_diagram() -> None:
    phase_3 = _phase_text("### Phase 3: OpenWebUI Integration", "### Phase 4:")

    assert ".plans/2026-04-27-openwebui-rag-gateway-integration.md" in phase_3
    assert "flowchart LR" in phase_3
    assert "OpenWebUI demo UI" in phase_3
    assert "FastAPI RAG Gateway" in phase_3
    assert "Raw vLLM smoke-test path" in phase_3
    assert "OpenAI-compatible provider base URL" in phase_3


def test_phase_3_plan_file_exists_and_is_unignored() -> None:
    plan = PHASE_3_PLAN.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")

    assert "Title: OpenWebUI RAG Gateway Integration" in plan
    assert "Status: Draft" in plan
    assert "flowchart LR" in plan
    assert "!/.plans/2026-04-27-openwebui-rag-gateway-integration.md" in gitignore
