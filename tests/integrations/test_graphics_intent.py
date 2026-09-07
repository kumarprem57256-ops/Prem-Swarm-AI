from integrations.vfx_forge.intent_parser import GraphicsIntentParser


def test_energy_effect():
    parser = GraphicsIntentParser()

    result = parser.parse(
        "create an energy effect"
    )

    assert result["task_type"] == "effect"
    assert result["effect"] == "energy"


def test_smoke_effect():
    parser = GraphicsIntentParser()

    result = parser.parse(
        "make a cinematic smoke particle effect"
    )

    assert result["task_type"] == "effect"
    assert result["effect"] == "smoke"


def test_design_request():
    parser = GraphicsIntentParser()

    result = parser.parse(
        "design a futuristic cyber city"
    )

    assert result["task_type"] == "design"
