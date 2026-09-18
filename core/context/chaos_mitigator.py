"""
PILLAR #3 — Entropic Chaos Mitigation

Controls context growth inside a multi-agent swarm.

Goals:
- remove near-duplicate messages
- preserve high-value information
- preserve diverse information
- protect critical/error/decision records
- prefer recent information when value is similar
- produce deterministic, auditable results

This is NOT irreversible compression.
The original records should remain available to the memory layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence, Tuple
import re


_WORD_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class ContextItem:
    """One piece of swarm context."""

    item_id: str
    text: str

    # Semantic/operational importance supplied by the producer.
    importance: float = 0.5

    # Larger value means newer/more recent.
    recency: float = 0.5

    # Protects critical facts/errors/decisions from removal.
    priority: float = 0.0

    source_agent: str = ""

    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass
class MitigationResult:
    """Result of one entropy-mitigation pass."""

    kept: List[ContextItem]
    removed: List[ContextItem]

    # IDs of removed records and their representative.
    duplicate_map: Dict[str, str]

    original_count: int
    kept_count: int
    removed_count: int

    reduction_ratio: float
    redundancy_ratio: float

    diagnostics: Dict[str, object] = field(default_factory=dict)


class EntropicChaosMitigator:
    """
    Deterministic context reducer.

    Similarity uses word shingles / token overlap instead of an external
    embedding dependency. This keeps the first runtime version portable
    on Termux and offline environments.

    Later NEXUS versions can plug an embedding similarity provider into
    this interface without changing the result contract.
    """

    def __init__(
        self,
        *,
        similarity_threshold: float = 0.82,
        max_items: int = 100,
        preserve_priority: float = 0.90,
    ) -> None:
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError(
                "similarity_threshold must be between 0 and 1."
            )

        if max_items < 1:
            raise ValueError("max_items must be >= 1.")

        if not 0.0 <= preserve_priority <= 1.0:
            raise ValueError(
                "preserve_priority must be between 0 and 1."
            )

        self.similarity_threshold = similarity_threshold
        self.max_items = max_items
        self.preserve_priority = preserve_priority

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token.lower()
            for token in _WORD_RE.findall(text)
            if len(token) > 1
        }

    @classmethod
    def similarity(
        cls,
        left: str,
        right: str,
    ) -> float:
        """
        Jaccard token similarity.

        Returns [0, 1].
        """
        a = cls._tokens(left)
        b = cls._tokens(right)

        if not a and not b:
            return 1.0

        if not a or not b:
            return 0.0

        return len(a & b) / len(a | b)

    def _utility(self, item: ContextItem) -> float:
        """
        Utility used when choosing which near-duplicate survives.
        """
        importance = self._clamp(item.importance)
        recency = self._clamp(item.recency)
        priority = self._clamp(item.priority)

        return (
            importance * 0.50
            + recency * 0.20
            + priority * 0.30
        )

    def _protected(self, item: ContextItem) -> bool:
        return item.priority >= self.preserve_priority

    def mitigate(
        self,
        items: Iterable[ContextItem],
    ) -> MitigationResult:
        records = list(items)

        if not records:
            return MitigationResult(
                kept=[],
                removed=[],
                duplicate_map={},
                original_count=0,
                kept_count=0,
                removed_count=0,
                reduction_ratio=0.0,
                redundancy_ratio=0.0,
                diagnostics={"reason": "empty_context"},
            )

        # First pass: strongest representatives first.
        ordered = sorted(
            records,
            key=lambda item: (
                self._protected(item),
                self._utility(item),
                item.item_id,
            ),
            reverse=True,
        )

        kept: List[ContextItem] = []
        removed: List[ContextItem] = []
        duplicate_map: Dict[str, str] = {}

        for item in ordered:
            representative = None

            for existing in kept:
                similarity = self.similarity(
                    item.text,
                    existing.text,
                )

                if similarity >= self.similarity_threshold:
                    representative = existing
                    break

            if representative is None:
                kept.append(item)
                continue

            # If the new item is protected and the current representative
            # isn't, replace the representative.
            if self._protected(item) and not self._protected(representative):
                kept.remove(representative)
                kept.append(item)

                removed.append(representative)
                duplicate_map[
                    representative.item_id
                ] = item.item_id
            else:
                removed.append(item)
                duplicate_map[
                    item.item_id
                ] = representative.item_id

        # Hard capacity limit. Never evict protected records.
        if len(kept) > self.max_items:
            protected = [
                item
                for item in kept
                if self._protected(item)
            ]

            normal = [
                item
                for item in kept
                if not self._protected(item)
            ]

            normal.sort(
                key=lambda item: (
                    self._utility(item),
                    item.item_id,
                ),
                reverse=True,
            )

            available = max(
                0,
                self.max_items - len(protected),
            )

            overflow = normal[available:]

            kept = protected + normal[:available]
            removed.extend(overflow)

        # Stable ordering for downstream context assembly.
        kept.sort(
            key=lambda item: (
                -self._utility(item),
                item.item_id,
            )
        )

        removed.sort(
            key=lambda item: item.item_id
        )

        original_count = len(records)
        kept_count = len(kept)
        removed_count = len(removed)

        reduction_ratio = (
            removed_count / original_count
            if original_count
            else 0.0
        )

        duplicate_count = len(duplicate_map)

        redundancy_ratio = (
            duplicate_count / original_count
            if original_count
            else 0.0
        )

        diagnostics = {
            "similarity_algorithm": "token_jaccard",
            "similarity_threshold": self.similarity_threshold,
            "max_items": self.max_items,
            "protected_items": sum(
                1 for item in kept
                if self._protected(item)
            ),
            "duplicate_groups": len(set(duplicate_map.values())),
        }

        return MitigationResult(
            kept=kept,
            removed=removed,
            duplicate_map=duplicate_map,
            original_count=original_count,
            kept_count=kept_count,
            removed_count=removed_count,
            reduction_ratio=reduction_ratio,
            redundancy_ratio=redundancy_ratio,
            diagnostics=diagnostics,
        )

    def compact_text(
        self,
        items: Sequence[ContextItem],
    ) -> str:
        """
        Build a compact context payload from the surviving records.
        """
        result = self.mitigate(items)

        lines = []

        for item in result.kept:
            source = (
                f"[{item.source_agent}] "
                if item.source_agent
                else ""
            )

            lines.append(
                f"{source}{item.text.strip()}"
            )

        return "\n".join(lines)
