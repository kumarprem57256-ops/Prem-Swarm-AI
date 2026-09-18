"""
PREM SWARM AI
Pillar #4 — Neuro-Symbolic Synaptic Memory

Combines:
- Episodic memory
- Semantic memory
- Symbolic relationships
- Confidence
- Provenance
- Retrieval
- Reinforcement

Design goal:
Keep learned/associative memory and explicit symbolic knowledge
in one verifiable, structured memory layer.
"""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class MemoryNode:
    node_id: str
    memory_type: str
    content: str
    confidence: float
    provenance: str
    created_at: float
    updated_at: float
    reinforcement: float = 0.0


@dataclass
class MemoryEdge:
    edge_id: str
    source_id: str
    target_id: str
    relation: str
    weight: float
    provenance: str
    created_at: float


class NeuroSymbolicMemory:
    """
    Persistent neuro-symbolic memory graph.

    Memory model:
        Node = fact / experience / concept
        Edge = explicit relationship
        Confidence = belief strength
        Reinforcement = outcome-based learning signal
        Provenance = where the memory came from
    """

    VALID_TYPES = {
        "episodic",
        "semantic",
        "symbolic",
        "concept",
        "experience",
    }

    def __init__(self, db_path: str = "swarm_synaptic_memory.db"):
        self.db_path = str(Path(db_path))
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_nodes (
                    node_id TEXT PRIMARY KEY,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    provenance TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    reinforcement REAL NOT NULL DEFAULT 0.0
                )
                """
            )

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_edges (
                    edge_id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    weight REAL NOT NULL,
                    provenance TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )

            db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_memory_content
                ON memory_nodes(content)
                """
            )

            db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_memory_type
                ON memory_nodes(memory_type)
                """
            )

            db.commit()

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def store(
        self,
        content: str,
        memory_type: str = "semantic",
        confidence: float = 0.5,
        provenance: str = "unknown",
    ) -> MemoryNode:

        if not content or not content.strip():
            raise ValueError("Memory content cannot be empty.")

        if memory_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid memory_type={memory_type!r}. "
                f"Expected one of {sorted(self.VALID_TYPES)}"
            )

        now = time.time()

        node = MemoryNode(
            node_id=f"mem_{uuid.uuid4().hex}",
            memory_type=memory_type,
            content=content.strip(),
            confidence=self._clamp(confidence),
            provenance=provenance or "unknown",
            created_at=now,
            updated_at=now,
        )

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO memory_nodes
                (node_id, memory_type, content, confidence,
                 provenance, created_at, updated_at, reinforcement)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    node.node_id,
                    node.memory_type,
                    node.content,
                    node.confidence,
                    node.provenance,
                    node.created_at,
                    node.updated_at,
                    node.reinforcement,
                ),
            )
            db.commit()

        return node

    def link(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 0.5,
        provenance: str = "unknown",
    ) -> MemoryEdge:

        if not relation or not relation.strip():
            raise ValueError("Relation cannot be empty.")

        if source_id == target_id:
            raise ValueError("Self-links are not allowed.")

        with self._connect() as db:
            source = db.execute(
                "SELECT node_id FROM memory_nodes WHERE node_id=?",
                (source_id,),
            ).fetchone()

            target = db.execute(
                "SELECT node_id FROM memory_nodes WHERE node_id=?",
                (target_id,),
            ).fetchone()

        if not source or not target:
            raise KeyError("Both source_id and target_id must exist.")

        edge = MemoryEdge(
            edge_id=f"edge_{uuid.uuid4().hex}",
            source_id=source_id,
            target_id=target_id,
            relation=relation.strip(),
            weight=self._clamp(weight),
            provenance=provenance or "unknown",
            created_at=time.time(),
        )

        with self._connect() as db:
            db.execute(
                """
                INSERT INTO memory_edges
                (edge_id, source_id, target_id, relation,
                 weight, provenance, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    edge.edge_id,
                    edge.source_id,
                    edge.target_id,
                    edge.relation,
                    edge.weight,
                    edge.provenance,
                    edge.created_at,
                ),
            )
            db.commit()

        return edge

    def reinforce(
        self,
        node_id: str,
        reward: float,
    ) -> MemoryNode:

        with self._connect() as db:
            row = db.execute(
                """
                SELECT node_id, memory_type, content, confidence,
                       provenance, created_at, updated_at, reinforcement
                FROM memory_nodes
                WHERE node_id=?
                """,
                (node_id,),
            ).fetchone()

            if not row:
                raise KeyError(f"Memory node not found: {node_id}")

            old = float(row[7])
            new_reinforcement = max(-1.0, min(1.0, old + float(reward)))
            new_confidence = self._clamp(
                float(row[3]) + (float(reward) * 0.1)
            )
            now = time.time()

            db.execute(
                """
                UPDATE memory_nodes
                SET confidence=?,
                    reinforcement=?,
                    updated_at=?
                WHERE node_id=?
                """,
                (
                    new_confidence,
                    new_reinforcement,
                    now,
                    node_id,
                ),
            )
            db.commit()

        return self.get(node_id)

    def get(self, node_id: str) -> MemoryNode:
        with self._connect() as db:
            row = db.execute(
                """
                SELECT node_id, memory_type, content, confidence,
                       provenance, created_at, updated_at, reinforcement
                FROM memory_nodes
                WHERE node_id=?
                """,
                (node_id,),
            ).fetchone()

        if not row:
            raise KeyError(f"Memory node not found: {node_id}")

        return MemoryNode(*row)

    def retrieve(
        self,
        query: str,
        memory_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[MemoryNode]:

        if not query or not query.strip():
            return []

        limit = max(1, min(int(limit), 100))
        terms = [
            term.strip().lower()
            for term in query.split()
            if term.strip()
        ]

        with self._connect() as db:
            if memory_type:
                rows = db.execute(
                    """
                    SELECT node_id, memory_type, content, confidence,
                           provenance, created_at, updated_at, reinforcement
                    FROM memory_nodes
                    WHERE memory_type=?
                    ORDER BY confidence DESC, reinforcement DESC,
                             updated_at DESC
                    LIMIT 100
                    """,
                    (memory_type,),
                ).fetchall()
            else:
                rows = db.execute(
                    """
                    SELECT node_id, memory_type, content, confidence,
                           provenance, created_at, updated_at, reinforcement
                    FROM memory_nodes
                    ORDER BY confidence DESC, reinforcement DESC,
                             updated_at DESC
                    LIMIT 100
                    """
                ).fetchall()

        scored = []

        for row in rows:
            content = row[2].lower()

            matches = sum(
                1 for term in terms
                if term in content
            )

            if matches == 0:
                continue

            score = (
                matches
                + float(row[3])
                + float(row[7])
            )

            scored.append((score, MemoryNode(*row)))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [node for _, node in scored[:limit]]

    def neighbors(
        self,
        node_id: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:

        limit = max(1, min(int(limit), 100))

        with self._connect() as db:
            rows = db.execute(
                """
                SELECT
                    e.edge_id,
                    e.source_id,
                    e.target_id,
                    e.relation,
                    e.weight,
                    e.provenance,
                    e.created_at
                FROM memory_edges e
                WHERE e.source_id=? OR e.target_id=?
                ORDER BY e.weight DESC
                LIMIT ?
                """,
                (node_id, node_id, limit),
            ).fetchall()

        return [
            {
                "edge_id": row[0],
                "source_id": row[1],
                "target_id": row[2],
                "relation": row[3],
                "weight": row[4],
                "provenance": row[5],
                "created_at": row[6],
            }
            for row in rows
        ]

    def export_graph(self) -> dict[str, Any]:
        with self._connect() as db:
            nodes = db.execute(
                """
                SELECT node_id, memory_type, content, confidence,
                       provenance, created_at, updated_at, reinforcement
                FROM memory_nodes
                """
            ).fetchall()

            edges = db.execute(
                """
                SELECT edge_id, source_id, target_id, relation,
                       weight, provenance, created_at
                FROM memory_edges
                """
            ).fetchall()

        return {
            "nodes": [
                asdict(MemoryNode(*row))
                for row in nodes
            ],
            "edges": [
                asdict(MemoryEdge(*row))
                for row in edges
            ],
        }

    def stats(self) -> dict[str, int]:
        with self._connect() as db:
            nodes = db.execute(
                "SELECT COUNT(*) FROM memory_nodes"
            ).fetchone()[0]

            edges = db.execute(
                "SELECT COUNT(*) FROM memory_edges"
            ).fetchone()[0]

        return {
            "nodes": int(nodes),
            "edges": int(edges),
        }
