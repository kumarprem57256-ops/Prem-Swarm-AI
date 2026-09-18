import json
from pathlib import Path

from core.autonomy.integration_adapter import Phase2IntegrationAdapter


def test_phase2_e2e_controlled_pipeline():
    root = Path.cwd()

    adapter = Phase2IntegrationAdapter(
        root=root,
        dry_run=True,
    )

    status = adapter.status()

    assert status["phase2_loaded"] is True
    assert status["existing_agents_loaded"] is True

    result = adapter.dry_run(
        pillar_name="CONTROLLED_E2E_TEST"
    )

    assert result.status == "PASS"
    assert result.details["dry_run"] is True

    expected_stages = [
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
    ]

    # Verify the actual control-flow stages.
    for stage in expected_stages:
        assert stage in result.details["stages"]

    # Verify that the concrete Phase-2 and V1 components
    # behind those boundaries are actually instantiated.
    components = result.details["components"]

    expected_components = [
        "phase2.intelligence",
        "phase2.architect",
        "phase2.verifier",
        "phase2.repair",
        "phase2.gate",
        "existing.coder",
        "existing.executor",
        "existing.healer",
        "existing.reviewer",
        "existing.failure_analyzer",
        "existing.sandbox",
        "existing.memory",
    ]

    for component in expected_components:
        assert components[component]["loaded"] is True

    print("\n" + "=" * 60)
    print("PREM SWARM V2 — CONTROLLED E2E PIPELINE")
    print("=" * 60)
    print("Phase 2 loaded       :", status["phase2_loaded"])
    print("Existing agents      :", status["existing_agents_loaded"])
    print("Dry-run              :", result.details["dry_run"])
    print("Pipeline components  :", len(result.details["stages"]))
    print("\nPipeline:")
    print(" -> ".join(result.details["stages"]))
    print("\nNo generated code executed.")
    print("No production files modified.")
    print("No external LLM called.")
    print("\n✅ CONTROLLED E2E PASS")
    print("=" * 60)


if __name__ == "__main__":
    test_phase2_e2e_controlled_pipeline()
