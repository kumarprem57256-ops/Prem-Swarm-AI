from core.consensus.quantum_consensus import (
    CandidateEvidence,
    QuantumConsensusMatrix,
)


def test_empty_consensus():
    engine = QuantumConsensusMatrix()

    result = engine.decide([])

    assert result.winner is None
    assert result.accepted is False
    assert result.evidence_count == 0


def test_strong_independent_consensus():
    engine = QuantumConsensusMatrix(
        acceptance_threshold=0.60,
        minimum_margin=0.05,
        minimum_agents=2,
    )

    result = engine.decide([
        CandidateEvidence(
            "planner",
            "A",
            0.90,
            evidence_quality=0.95,
            agent_reliability=0.95,
            independence=1.0,
        ),
        CandidateEvidence(
            "researcher",
            "A",
            0.88,
            evidence_quality=0.90,
            agent_reliability=0.90,
            independence=0.95,
        ),
        CandidateEvidence(
            "critic",
            "B",
            0.30,
            evidence_quality=0.80,
            agent_reliability=0.80,
            independence=1.0,
        ),
    ])

    assert result.winner == "A"
    assert result.accepted is True
    assert result.confidence > 0.60
    assert result.margin > 0
    assert result.agent_count == 3


def test_correlation_reduces_duplicate_influence():
    engine = QuantumConsensusMatrix(
        acceptance_threshold=0.70,
        minimum_margin=0.0,
    )

    result = engine.decide([
        CandidateEvidence(
            "agent_1",
            "A",
            0.95,
            independence=1.0,
        ),
        CandidateEvidence(
            "agent_2",
            "A",
            0.95,
            independence=0.05,
        ),
        CandidateEvidence(
            "agent_3",
            "B",
            0.80,
            independence=1.0,
        ),
    ])

    assert result.winner == "A"
    assert result.diagnostics["independence_aware"] is True


def test_disagreement_is_detected():
    engine = QuantumConsensusMatrix()

    result = engine.decide([
        CandidateEvidence("a", "A", 0.99),
        CandidateEvidence("b", "B", 0.99),
        CandidateEvidence("c", "A", 0.01),
        CandidateEvidence("d", "B", 0.01),
    ])

    assert result.disagreement > 0


def test_low_margin_is_not_accepted():
    engine = QuantumConsensusMatrix(
        acceptance_threshold=0.45,
        minimum_margin=0.20,
    )

    result = engine.decide([
        CandidateEvidence("a", "A", 0.55),
        CandidateEvidence("b", "B", 0.52),
    ])

    assert result.accepted is False


def test_top_candidates_are_sorted():
    engine = QuantumConsensusMatrix()

    result = engine.decide([
        CandidateEvidence("a", "A", 0.9),
        CandidateEvidence("b", "B", 0.5),
        CandidateEvidence("c", "C", 0.2),
    ])

    top = result.top(3)

    assert top[0][0] == "A"
    assert len(top) == 3
