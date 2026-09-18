from pathlib import Path

from core.memory.memory_integration_adapter import (
    MemoryIntegrationAdapter,
)
from core.memory.neuro_symbolic_memory import (
    NeuroSymbolicMemory,
)


def test_adapter_store_recall(tmp_path: Path):
    memory = NeuroSymbolicMemory(
        str(tmp_path / "synaptic.db")
    )

    adapter = MemoryIntegrationAdapter(
        synaptic_memory=memory
    )

    node = adapter.remember(
        "Fractal Planner improves hierarchical task planning",
        memory_type="semantic",
        confidence=0.9,
        provenance="pillar1",
    )

    results = adapter.recall("Fractal Planner")

    assert node.node_id
    assert len(results) == 1
    assert results[0].node_id == node.node_id


def test_adapter_symbolic_learning(tmp_path: Path):
    memory = NeuroSymbolicMemory(
        str(tmp_path / "synaptic.db")
    )

    adapter = MemoryIntegrationAdapter(
        synaptic_memory=memory
    )

    planner = adapter.remember(
        "Fractal Planner",
        memory_type="concept",
        confidence=0.7,
    )

    memory_node = adapter.remember(
        "Neuro-Symbolic Memory",
        memory_type="concept",
        confidence=0.8,
    )

    edge = adapter.connect(
        planner.node_id,
        memory_node.node_id,
        "related_to",
        weight=0.85,
    )

    updated = adapter.learn_from_result(
        planner.node_id,
        0.5,
    )

    assert edge.relation == "related_to"
    assert updated.reinforcement > 0
    assert updated.confidence > 0.7


def test_adapter_graph(tmp_path: Path):
    memory = NeuroSymbolicMemory(
        str(tmp_path / "synaptic.db")
    )

    adapter = MemoryIntegrationAdapter(
        synaptic_memory=memory
    )

    a = adapter.remember("Planning")
    b = adapter.remember("Memory")

    adapter.connect(
        a.node_id,
        b.node_id,
        "supports",
    )

    graph = adapter.graph()

    assert len(graph["nodes"]) == 2
    assert len(graph["edges"]) == 1


def test_adapter_status(tmp_path: Path):
    memory = NeuroSymbolicMemory(
        str(tmp_path / "synaptic.db")
    )

    adapter = MemoryIntegrationAdapter(
        synaptic_memory=memory
    )

    status = adapter.status()

    assert status["pillar"] == 4
    assert status["synaptic_memory"] is True
    assert status["legacy_memory_connected"] is False
    assert status["nodes"] == 0
    assert status["edges"] == 0


def test_legacy_memory_can_be_attached(tmp_path: Path):
    memory = NeuroSymbolicMemory(
        str(tmp_path / "synaptic.db")
    )

    fake_legacy = object()

    adapter = MemoryIntegrationAdapter(
        synaptic_memory=memory,
        legacy_memory=fake_legacy,
    )

    status = adapter.status()

    assert status["legacy_memory_connected"] is True
