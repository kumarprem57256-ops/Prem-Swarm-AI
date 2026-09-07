from integrations.vfx_forge.task_router import GraphicsTaskRouter


def test_router_detects_graphics_request():
    router = GraphicsTaskRouter()

    assert router.can_handle(
        "create a cinematic graphics design"
    )


def test_router_classifies_effect():
    router = GraphicsTaskRouter()

    assert router.classify(
        "create an energy particle effect"
    ) == "effect"


def test_router_classifies_design():
    router = GraphicsTaskRouter()

    assert router.classify(
        "create a cinematic cyber design"
    ) == "design"


def test_router_ignores_unrelated_request():
    router = GraphicsTaskRouter()

    result = router.route(
        "calculate 25 + 25"
    )

    assert result["handled"] is False
    assert result["agent"] is None


def test_router_executes_vfx():
    router = GraphicsTaskRouter()

    result = router.route(
        "create an energy effect"
    )

    assert result["agent"] == "graphics_vfx_agent"
    assert result["task_type"] == "effect"
    assert result["result"]["name"] == "VFX_energy"
