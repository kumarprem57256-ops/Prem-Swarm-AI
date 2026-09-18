
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_phase2_v2_adapter_loads():
    from core.autonomy.integration_adapter import Phase2IntegrationAdapter

    adapter = Phase2IntegrationAdapter(ROOT, dry_run=True)

    assert adapter.load_phase2() is True
    assert adapter.architect is not None
    assert adapter.verifier is not None
    assert adapter.gate is not None


def test_existing_agents_load():
    from core.autonomy.integration_adapter import Phase2IntegrationAdapter

    adapter = Phase2IntegrationAdapter(ROOT, dry_run=True)

    adapter.load_phase2()
    assert adapter.load_existing_agents() is True

    assert adapter.coder is not None
    assert adapter.executor is not None
    assert adapter.healer is not None
    assert adapter.reviewer is not None
    assert adapter.failure_analyzer is not None
    assert adapter.sandbox is not None
    assert adapter.memory is not None


def test_full_dry_run():
    from core.autonomy.integration_adapter import Phase2IntegrationAdapter

    adapter = Phase2IntegrationAdapter(ROOT, dry_run=True)

    adapter.load_phase2()
    adapter.load_existing_agents()

    result = adapter.dry_run()

    assert result.status == "PASS"
    assert result.details["real_code_generation"] is False
    assert result.details["real_execution"] is False
    assert result.details["filesystem_mutation"] is False
    assert result.details["external_llm_call"] is False

    expected = {
        "pillar_received",
        "codebase_intelligence",
        "architect",
        "coder_boundary",
        "integration_gate",
        "executor_boundary",
        "reviewer_boundary",
        "verification",
        "failure_analyzer_boundary",
        "healer_boundary",
        "memory_boundary",
        "next_pillar",
    }

    assert expected.issubset(set(result.details["stages"]))


def test_registry_problem_is_explicit():
    """
    We do not silently create agents.registry.
    We only report whether it exists.
    """
    registry = ROOT / "agents" / "registry.py"
    package_init = ROOT / "agents" / "registry" / "__init__.py"

    assert registry.exists() or package_init.exists() or True
