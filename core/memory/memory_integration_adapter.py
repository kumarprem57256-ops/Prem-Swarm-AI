"""
Pillar #4 integration adapter.

Bridges the new NeuroSymbolicMemory layer with the existing
PREM MemoryCore without replacing or modifying MemoryCore.
"""

from __future__ import annotations

from typing import Any, Optional

from .neuro_symbolic_memory import NeuroSymbolicMemory


class MemoryIntegrationAdapter:
    def __init__(
        self,
        synaptic_memory: Optional[NeuroSymbolicMemory] = None,
        legacy_memory: Any = None,
    ):
        self.synaptic = synaptic_memory or NeuroSymbolicMemory()
        self.legacy = legacy_memory

    def remember(
        self,
        content: str,
        memory_type: str = "semantic",
        confidence: float = 0.5,
        provenance: str = "integration",
    ):
        """
        Store knowledge in the new neuro-symbolic layer.

        Legacy MemoryCore is optional and is never required for the
        synaptic layer to function.
        """
        node = self.synaptic.store(
            content=content,
            memory_type=memory_type,
            confidence=confidence,
            provenance=provenance,
        )

        return node

    def connect(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 0.5,
        provenance: str = "integration",
    ):
        return self.synaptic.link(
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            weight=weight,
            provenance=provenance,
        )

    def learn_from_result(
        self,
        node_id: str,
        reward: float,
    ):
        """
        Reinforce memory after a verified outcome.
        """
        return self.synaptic.reinforce(node_id, reward)

    def recall(
        self,
        query: str,
        limit: int = 10,
    ):
        return self.synaptic.retrieve(
            query=query,
            limit=limit,
        )

    def graph(self):
        return self.synaptic.export_graph()

    def status(self) -> dict:
        stats = self.synaptic.stats()

        return {
            "adapter": "MemoryIntegrationAdapter",
            "pillar": 4,
            "synaptic_memory": True,
            "legacy_memory_connected": self.legacy is not None,
            "nodes": stats["nodes"],
            "edges": stats["edges"],
        }
