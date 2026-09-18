from core.context.chaos_mitigator import (
    ContextItem,
    EntropicChaosMitigator,
)


def test_empty_context():
    engine = EntropicChaosMitigator()

    result = engine.mitigate([])

    assert result.original_count == 0
    assert result.kept_count == 0
    assert result.removed_count == 0


def test_near_duplicates_are_removed():
    engine = EntropicChaosMitigator(
        similarity_threshold=0.75,
    )

    result = engine.mitigate([
        ContextItem(
            "a",
            "The planner selected Python for the implementation.",
            importance=0.8,
            recency=0.8,
        ),
        ContextItem(
            "b",
            "Planner selected Python for implementation.",
            importance=0.5,
            recency=0.5,
        ),
        ContextItem(
            "c",
            "The database schema requires three tables.",
            importance=0.7,
            recency=0.7,
        ),
    ])

    assert result.kept_count == 2
    assert result.removed_count == 1
    assert "b" in result.duplicate_map


def test_important_distinct_context_survives():
    engine = EntropicChaosMitigator()

    result = engine.mitigate([
        ContextItem(
            "decision",
            "The deployment target is Android Termux.",
            importance=1.0,
            priority=1.0,
        ),
        ContextItem(
            "error",
            "The previous execution failed because the module was missing.",
            importance=1.0,
            priority=1.0,
        ),
    ])

    ids = {item.item_id for item in result.kept}

    assert ids == {"decision", "error"}


def test_protected_item_replaces_unprotected_duplicate():
    engine = EntropicChaosMitigator(
        similarity_threshold=0.70,
    )

    result = engine.mitigate([
        ContextItem(
            "normal",
            "The build failed due to a missing module.",
            importance=0.4,
            priority=0.1,
        ),
        ContextItem(
            "critical",
            "The build failed due to a missing module.",
            importance=0.7,
            priority=1.0,
        ),
    ])

    ids = {item.item_id for item in result.kept}

    assert "critical" in ids
    assert "normal" not in ids


def test_capacity_limit():
    engine = EntropicChaosMitigator(
        max_items=3,
    )

    items = [
        ContextItem(
            f"item-{i}",
            f"Unique context statement number {i}",
            importance=i / 10,
            recency=i / 10,
        )
        for i in range(10)
    ]

    result = engine.mitigate(items)

    assert result.kept_count <= 3
    assert result.removed_count >= 7


def test_similarity_is_symmetric():
    left = "agent planner selected Python"
    right = "planner agent selected Python"

    a = EntropicChaosMitigator.similarity(left, right)
    b = EntropicChaosMitigator.similarity(right, left)

    assert a == b
    assert 0.0 <= a <= 1.0


def test_compact_text_contains_survivors():
    engine = EntropicChaosMitigator()

    items = [
        ContextItem(
            "a",
            "Mission architecture approved.",
            source_agent="planner",
        ),
        ContextItem(
            "b",
            "Execution requires verification.",
            source_agent="critic",
        ),
    ]

    text = engine.compact_text(items)

    assert "Mission architecture approved." in text
    assert "Execution requires verification." in text
    assert "[planner]" in text
