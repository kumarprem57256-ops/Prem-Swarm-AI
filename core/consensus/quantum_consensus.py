"""
PILLAR #2 — QuantumConsensus Matrix

A confidence/probability-based consensus engine for NEXUS.

Important:
- "Quantum" is an architectural name, not a claim of quantum computing.
- Agents do NOT need to exchange their complete outputs.
- Each agent can submit compact evidence:
    candidate + confidence + evidence quality + reliability + independence
- The engine combines these signals using weighted log-opinion pooling.
- No external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import log, exp
from typing import Dict, Iterable, List, Optional


_EPS = 1e-12


@dataclass(frozen=True)
class CandidateEvidence:
    """Compact belief update supplied by one agent."""

    agent_id: str
    candidate_id: str
    confidence: float

    # Quality of the evidence supporting this belief.
    evidence_quality: float = 1.0

    # Historical reliability of this agent for the current capability.
    agent_reliability: float = 1.0

    # Independence from other agents.
    # 1.0 = independent, 0.0 = almost fully correlated.
    independence: float = 1.0

    # Optional compact reason/evidence reference.
    evidence_ref: Optional[str] = None

    metadata: Dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "confidence",
            self._clamp(self.confidence),
        )
        object.__setattr__(
            self,
            "evidence_quality",
            self._clamp(self.evidence_quality),
        )
        object.__setattr__(
            self,
            "agent_reliability",
            self._clamp(self.agent_reliability),
        )
        object.__setattr__(
            self,
            "independence",
            self._clamp(self.independence),
        )

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    @property
    def weight(self) -> float:
        """
        Effective contribution weight.

        Reliability, evidence quality and independence all matter.
        A correlated swarm should not gain confidence merely because
        many agents repeated the same information.
        """
        return (
            self.evidence_quality
            * self.agent_reliability
            * self.independence
        )


@dataclass
class ConsensusResult:
    """Auditable result returned by the consensus matrix."""

    winner: Optional[str]
    probabilities: Dict[str, float]
    confidence: float

    # Difference between strongest and second strongest candidate.
    margin: float

    # How much disagreement exists among submitted evidence.
    disagreement: float

    # Number of unique agents contributing.
    agent_count: int

    # Number of evidence records.
    evidence_count: int

    accepted: bool

    threshold: float

    contributors: Dict[str, List[str]] = field(default_factory=dict)
    diagnostics: Dict[str, object] = field(default_factory=dict)

    def top(self, n: int = 3) -> List[tuple[str, float]]:
        return sorted(
            self.probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:n]


class ConsensusMatrix:
    """
    Immutable-ish result model.

    Kept separate from the engine so future NEXUS telemetry/storage
    layers can consume a stable result contract.
    """

    def __init__(
        self,
        result: ConsensusResult,
    ) -> None:
        self.result = result


class QuantumConsensusMatrix:
    """
    Confidence-based swarm consensus engine.

    Algorithm:
      1. Group evidence by candidate.
      2. Weight each observation by:
           evidence_quality
           × agent_reliability
           × independence
      3. Combine beliefs using weighted log opinion pooling.
      4. Normalize candidate scores.
      5. Measure disagreement and winner margin.
      6. Accept only when the configured confidence threshold is met.
    """

    def __init__(
        self,
        *,
        acceptance_threshold: float = 0.60,
        minimum_margin: float = 0.05,
        minimum_agents: int = 1,
    ) -> None:
        if not 0.0 <= acceptance_threshold <= 1.0:
            raise ValueError("acceptance_threshold must be between 0 and 1.")

        if not 0.0 <= minimum_margin <= 1.0:
            raise ValueError("minimum_margin must be between 0 and 1.")

        if minimum_agents < 1:
            raise ValueError("minimum_agents must be >= 1.")

        self.acceptance_threshold = acceptance_threshold
        self.minimum_margin = minimum_margin
        self.minimum_agents = minimum_agents

    @staticmethod
    def _normalize(values: Dict[str, float]) -> Dict[str, float]:
        total = sum(values.values())

        if total <= _EPS:
            if not values:
                return {}
            equal = 1.0 / len(values)
            return {key: equal for key in values}

        return {
            key: value / total
            for key, value in values.items()
        }

    @staticmethod
    def _safe_probability(value: float) -> float:
        return max(_EPS, min(1.0 - _EPS, float(value)))

    def _candidate_score(
        self,
        records: Iterable[CandidateEvidence],
    ) -> float:
        """
        Weighted log-opinion pooling.

        This rewards strong independent evidence while preventing
        simple duplicate-agent counting from becoming linear certainty.
        """
        score = 0.0
        total_weight = 0.0

        for record in records:
            weight = record.weight

            if weight <= _EPS:
                continue

            probability = self._safe_probability(record.confidence)

            score += weight * log(probability)
            total_weight += weight

        if total_weight <= _EPS:
            return 0.0

        return exp(score / total_weight)

    def _disagreement(
        self,
        evidence: List[CandidateEvidence],
    ) -> float:
        """
        Weighted disagreement in [0, 1].

        0 = strong agreement.
        1 = maximally conflicting beliefs.
        """
        if len(evidence) <= 1:
            return 0.0

        total_weight = sum(item.weight for item in evidence)

        if total_weight <= _EPS:
            return 1.0

        weighted_mean = sum(
            item.confidence * item.weight
            for item in evidence
        ) / total_weight

        variance = sum(
            item.weight * (item.confidence - weighted_mean) ** 2
            for item in evidence
        ) / total_weight

        # Bernoulli variance maximum is 0.25.
        return max(0.0, min(1.0, variance / 0.25))

    def decide(
        self,
        evidence: Iterable[CandidateEvidence],
    ) -> ConsensusResult:
        records = list(evidence)

        if not records:
            return ConsensusResult(
                winner=None,
                probabilities={},
                confidence=0.0,
                margin=0.0,
                disagreement=0.0,
                agent_count=0,
                evidence_count=0,
                accepted=False,
                threshold=self.acceptance_threshold,
                diagnostics={"reason": "no_evidence"},
            )

        candidates: Dict[str, List[CandidateEvidence]] = {}

        for record in records:
            if not record.candidate_id:
                continue

            candidates.setdefault(record.candidate_id, []).append(record)

        if not candidates:
            return ConsensusResult(
                winner=None,
                probabilities={},
                confidence=0.0,
                margin=0.0,
                disagreement=1.0,
                agent_count=len({r.agent_id for r in records}),
                evidence_count=len(records),
                accepted=False,
                threshold=self.acceptance_threshold,
                diagnostics={"reason": "no_valid_candidates"},
            )

        raw_scores = {
            candidate: self._candidate_score(items)
            for candidate, items in candidates.items()
        }

        probabilities = self._normalize(raw_scores)

        ranked = sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        winner = ranked[0][0]
        confidence = ranked[0][1]

        second_probability = (
            ranked[1][1]
            if len(ranked) > 1
            else 0.0
        )

        margin = confidence - second_probability

        disagreement = self._disagreement(records)

        unique_agents = {
            record.agent_id
            for record in records
            if record.agent_id
        }

        accepted = (
            len(unique_agents) >= self.minimum_agents
            and confidence >= self.acceptance_threshold
            and margin >= self.minimum_margin
        )

        contributors = {
            candidate: sorted({
                record.agent_id
                for record in items
                if record.agent_id
            })
            for candidate, items in candidates.items()
        }

        diagnostics = {
            "algorithm": "weighted_log_opinion_pooling",
            "independence_aware": True,
            "duplicate_vote_resistance": True,
            "unique_agents": len(unique_agents),
            "candidate_count": len(candidates),
            "acceptance_threshold": self.acceptance_threshold,
            "minimum_margin": self.minimum_margin,
            "minimum_agents": self.minimum_agents,
        }

        return ConsensusResult(
            winner=winner,
            probabilities=probabilities,
            confidence=confidence,
            margin=margin,
            disagreement=disagreement,
            agent_count=len(unique_agents),
            evidence_count=len(records),
            accepted=accepted,
            threshold=self.acceptance_threshold,
            contributors=contributors,
            diagnostics=diagnostics,
        )

    def consensus(
        self,
        evidence: Iterable[CandidateEvidence],
    ) -> ConsensusMatrix:
        return ConsensusMatrix(self.decide(evidence))
