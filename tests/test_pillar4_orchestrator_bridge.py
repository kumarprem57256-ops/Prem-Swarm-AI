from pathlib import Path

from core.memory.orchestrator_memory_bridge import (
    OrchestratorMemoryBridge,
)


def test_success_learning_bridge(tmp_path: Path):
    bridge = OrchestratorMemoryBridge(
        db_path=str(tmp_path / "synaptic.db")
    )

    result = bridge.record_success(
        topic="calculator tool",
        solution="generated and verified successfully",
    )

    assert result["status"] == "PASS"
    assert result["event"] == "success"
    assert result["node_id"]
    assert result["reinforcement"] > 0


def test_failure_learning_bridge(tmp_path: Path):
    bridge = OrchestratorMemoryBridge(
        db_path=str(tmp_path / "synaptic.db")
    )

    result = bridge.record_failure(
        topic="calculator tool",
        error_type="SyntaxError",
        solution="corrected generated source",
    )

    assert result["status"] == "PASS"
    assert result["event"] == "failure_learning"
    assert result["node_id"]


def test_recall_for_future_task(tmp_path: Path):
    bridge = OrchestratorMemoryBridge(
        db_path=str(tmp_path / "synaptic.db")
    )

    bridge.record_success(
        topic="calculator tool",
        solution="verified implementation",
    )

    memories = bridge.recall_for_task(
        "calculator"
    )

    assert memories
    assert memories[0]["node_id"]
    assert memories[0]["confidence"] > 0


def test_legacy_memory_is_preserved(tmp_path: Path):
    fake_legacy = object()

    bridge = OrchestratorMemoryBridge(
        legacy_memory=fake_legacy,
        db_path=str(tmp_path / "synaptic.db"),
    )

    status = bridge.status()

    assert status["legacy_memory_connected"] is True
    assert status["legacy_memory_preserved"] is True
    assert status["synaptic_memory"] is True


def test_bridge_does_not_require_legacy_memory(tmp_path: Path):
    bridge = OrchestratorMemoryBridge(
        legacy_memory=None,
        db_path=str(tmp_path / "synaptic.db"),
    )

    result = bridge.record_success(
        topic="test mission",
        solution="passed",
    )

    assert result["status"] == "PASS"
