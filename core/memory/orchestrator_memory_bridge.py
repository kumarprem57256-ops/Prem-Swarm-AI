"""
PREM SWARM AI
Pillar #4 — Orchestrator Memory Bridge

Keeps the existing MemoryCore learning path intact while adding
Neuro-Symbolic Synaptic Memory as a parallel verified layer.

The bridge is deliberately non-invasive:
- does not replace MemoryCore
- does not modify orchestrator.py
- failures in the new layer never break legacy learning
"""

from __future__ import annotations

from typing import Any, Optional

from .memory_integration_adapter import MemoryIntegrationAdapter
from .neuro_symbolic_memory import NeuroSymbolicMemory


class OrchestratorMemoryBridge:

    def __init__(
        self,
        legacy_memory: Optional[Any] = None,
        db_path: str = "swarm_synaptic_memory.db",
    ):
        self.legacy_memory = legacy_memory

        self.synaptic_memory = NeuroSymbolicMemory(
            db_path=db_path
        )

        self.adapter = MemoryIntegrationAdapter(
            synaptic_memory=self.synaptic_memory,
            legacy_memory=legacy_memory,
        )

    def record_success(
        self,
        topic: str,
        solution: str,
        confidence: float = 0.8,
        provenance: str = "orchestrator",
    ) -> dict:
        """
        Record a successful mission.

        Legacy MemoryCore remains responsible for its existing
        persistence path. The new layer stores a semantic/episodic
        representation and reinforces it positively.
        """

        node = self.adapter.remember(
            content=f"{topic}: {solution}",
            memory_type="episodic",
            confidence=confidence,
            provenance=provenance,
        )

        reinforced = self.adapter.learn_from_result(
            node.node_id,
            0.25,
        )

        return {
            "status": "PASS",
            "event": "success",
            "node_id": reinforced.node_id,
            "confidence": reinforced.confidence,
            "reinforcement": reinforced.reinforcement,
        }

    def record_failure(
        self,
        topic: str,
        error_type: str,
        solution: str,
        confidence: float = 0.6,
        provenance: str = "orchestrator",
    ) -> dict:
        """
        Record a failure and its eventual solution.

        The memory is stored as an experience rather than silently
        treating the failure itself as truth.
        """

        node = self.adapter.remember(
            content=(
                f"{topic} | "
                f"error={error_type} | "
                f"solution={solution}"
            ),
            memory_type="experience",
            confidence=confidence,
            provenance=provenance,
        )

        return {
            "status": "PASS",
            "event": "failure_learning",
            "node_id": node.node_id,
            "confidence": node.confidence,
        }

    def recall_for_task(
        self,
        task: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Retrieve relevant previous experiences for a new task.
        """

        memories = self.adapter.recall(
            query=task,
            limit=limit,
        )

        return [
            {
                "node_id": node.node_id,
                "memory_type": node.memory_type,
                "content": node.content,
                "confidence": node.confidence,
                "reinforcement": node.reinforcement,
                "provenance": node.provenance,
            }
            for node in memories
        ]

    def status(self) -> dict:
        result = self.adapter.status()

        result.update(
            {
                "bridge": "OrchestratorMemoryBridge",
                "legacy_memory_preserved": True,
            }
        )

        return result
