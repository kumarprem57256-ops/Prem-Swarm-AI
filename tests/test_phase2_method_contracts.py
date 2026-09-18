from pathlib import Path

from core.autonomy.integration_adapter import Phase2IntegrationAdapter


def test_method_to_method_contracts():
    adapter = Phase2IntegrationAdapter(
        root=Path.cwd(),
        dry_run=True,
    )

    # Phase 2 methods
    assert callable(adapter.intelligence.scan)
    assert callable(adapter.intelligence.relevant_context)

    assert callable(adapter.architect.create_plan)

    assert callable(adapter.verifier.run)
    assert callable(adapter.verifier.all)

    assert callable(adapter.repair.propose)

    assert callable(adapter.gate.allowed)
    assert callable(adapter.gate.backup)
    assert callable(adapter.gate.snapshot_hash)

    # Existing V1 methods
    assert callable(adapter.coder.build_tool)
    assert callable(adapter.executor.execute)
    assert callable(adapter.healer.diagnose_and_fix)
    assert callable(adapter.reviewer.review_code)
    assert callable(adapter.failure_analyzer.analyze_failure)
    assert callable(adapter.sandbox.Execute_and_benchmark)
    assert callable(adapter.memory.save_learning)

    # Adapter-level controlled flow
    result = adapter.dry_run(
        pillar_name="METHOD_CONTRACT_TEST"
    )

    assert result.status == "PASS"
    assert result.details["dry_run"] is True
    assert result.details["real_code_generation"] is False
    assert result.details["real_execution"] is False
    assert result.details["filesystem_mutation"] is False
    assert result.details["external_llm_call"] is False

    print("\n" + "=" * 64)
    print("PREM SWARM V2 — METHOD CONTRACT TEST")
    print("=" * 64)
    print("Phase 2 methods     : PASS")
    print("V1 agent methods    : PASS")
    print("Adapter flow        : PASS")
    print("Code generation     : DISABLED")
    print("Code execution      : DISABLED")
    print("Filesystem mutation : DISABLED")
    print("External LLM        : DISABLED")
    print("\n✅ METHOD-TO-METHOD CONTRACT PASS")
    print("=" * 64)


if __name__ == "__main__":
    test_method_to_method_contracts()
