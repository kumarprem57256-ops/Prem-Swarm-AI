from integrations.vfx_forge.graphics_agent import GraphicsVFXAgent


def test_design_task():
    agent = GraphicsVFXAgent()

    result = agent.run(
        "design",
        "cinematic cyber city",
    )

    assert result["agent"] == "graphics_vfx_agent"
    assert result["task_type"] == "design"
    assert result["result"]["genre"] == "action"


def test_effect_task():
    agent = GraphicsVFXAgent()

    result = agent.run(
        "effect",
        "energy",
    )

    assert result["agent"] == "graphics_vfx_agent"
    assert result["task_type"] == "effect"
    assert result["result"]["name"] == "VFX_energy"


def test_invalid_task():
    agent = GraphicsVFXAgent()

    try:
        agent.run("unknown", "test")
        assert False
    except ValueError as exc:
        assert "Unsupported" in str(exc)
