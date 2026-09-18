from pathlib import Path

from core.memory.neuro_symbolic_memory import NeuroSymbolicMemory


def test_store_and_get(tmp_path: Path):
    memory = NeuroSymbolicMemory(str(tmp_path / "memory.db"))

    node = memory.store(
        "PREM uses Fractal Planner for hierarchical planning",
        memory_type="semantic",
        confidence=0.9,
        provenance="pillar1",
    )

    loaded = memory.get(node.node_id)

    assert loaded.node_id == node.node_id
    assert loaded.memory_type == "semantic"
    assert loaded.confidence == 0.9
    assert "Fractal Planner" in loaded.content


def test_symbolic_link_and_neighbors(tmp_path: Path):
    memory = NeuroSymbolicMemory(str(tmp_path / "memory.db"))

    planner = memory.store(
        "Fractal Planner",
        memory_type="concept",
        confidence=0.9,
        provenance="core",
    )

    context = memory.store(
        "Context Compaction",
        memory_type="concept",
        confidence=0.8,
        provenance="core",
    )

    edge = memory.link(
        planner.node_id,
        context.node_id,
        "supports",
        weight=0.85,
        provenance="architecture",
    )

    neighbors = memory.neighbors(planner.node_id)

    assert edge.source_id == planner.node_id
    assert edge.target_id == context.node_id
    assert neighbors
    assert neighbors[0]["relation"] == "supports"


def test_retrieval_and_reinforcement(tmp_path: Path):
    memory = NeuroSymbolicMemory(str(tmp_path / "memory.db"))

    node = memory.store(
        "Successful calculator tool generation",
        memory_type="episodic",
        confidence=0.5,
        provenance="execution",
    )

    results = memory.retrieve("calculator generation")

    assert results
    assert results[0].node_id == node.node_id

    updated = memory.reinforce(node.node_id, 0.5)

    assert updated.reinforcement > 0
    assert updated.confidence > 0.5


def test_export_and_stats(tmp_path: Path):
    memory = NeuroSymbolicMemory(str(tmp_path / "memory.db"))

    a = memory.store(
        "Planner",
        memory_type="concept",
        provenance="test",
    )

    b = memory.store(
        "Memory",
        memory_type="concept",
        provenance="test",
    )

    memory.link(a.node_id, b.node_id, "related_to")

    stats = memory.stats()
    graph = memory.export_graph()

    assert stats["nodes"] == 2
    assert stats["edges"] == 1
    assert len(graph["nodes"]) == 2
    assert len(graph["edges"]) == 1


def test_invalid_memory_type_is_rejected(tmp_path: Path):
    memory = NeuroSymbolicMemory(str(tmp_path / "memory.db"))

    try:
        memory.store(
            "invalid",
            memory_type="unknown",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid memory type was accepted")
