from integrations.vfx_forge.adapter import VFXForgeAdapter


def test_vfx_forge_available():
    vfx = VFXForgeAdapter()

    status = vfx.status()

    assert status["available"] is True
    assert status["name"] == "PREM-VFX-FORGE"


def test_create_design():
    vfx = VFXForgeAdapter()

    result = vfx.create_design("cinematic cyber city")

    assert result["project_name"] == "PREM VFX PROJECT"
    assert result["genre"] == "action"
    assert "environment" in result["assets"]
    assert "particles" in result["vfx"]


def test_create_vfx_effect():
    vfx = VFXForgeAdapter()

    result = vfx.create_effect("energy")

    assert result["name"] == "VFX_energy"
    assert result["type"] == "particle"
    assert result["effect"] == "energy"
    assert result["status"] == "generated"
