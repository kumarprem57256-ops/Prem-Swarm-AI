from pathlib import Path
import subprocess
import sys
import json


VFX_ROOT = Path.home() / "PREM-VFX-FORGE"


class VFXForgeAdapter:
    """
    Isolated bridge between Prem Swarm AI and PREM-VFX-FORGE.

    VFX Forge runs in its own Python process so its internal
    packages (brain, agents, engine, generators, etc.) do not
    collide with Prem Swarm AI packages.
    """

    def __init__(self):
        self.root = VFX_ROOT

    def status(self):
        return {
            "available": self.root.exists(),
            "path": str(self.root),
            "name": "PREM-VFX-FORGE",
        }

    def _run_python(self, code):
        if not self.root.exists():
            raise RuntimeError("PREM-VFX-FORGE not found.")

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(self.root),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "VFX Forge execution failed:\n"
                + result.stderr.strip()
            )

        return result.stdout.strip()

    def create_design(self, idea):
        if not idea or not str(idea).strip():
            raise ValueError("Design idea cannot be empty.")

        payload = json.dumps(str(idea).strip())

        code = f"""
import json
from brain.director import CreativeDirector

idea = json.loads({payload!r})
plan = CreativeDirector().create_design(idea)

print(json.dumps({{
    "project_name": plan.project_name,
    "genre": plan.genre,
    "visual_style": plan.visual_style,
    "assets": plan.assets,
    "vfx": plan.vfx,
    "ui": plan.ui
}}))
"""

        output = self._run_python(code)
        return json.loads(output)

    def create_effect(self, effect):
        if not effect or not str(effect).strip():
            raise ValueError("Effect cannot be empty.")

        payload = json.dumps(str(effect).strip())

        code = f"""
import json
from agents.vfx_agent import VFXAgent

effect = json.loads({payload!r})
result = VFXAgent().create(effect)

print(json.dumps(result, default=str))
"""

        output = self._run_python(code)
        return json.loads(output)

    def generate_scene(self, size=5):
        code = f"""
import json
from engine.graphics_engine import GraphicsEngine

scene, report, output = GraphicsEngine().generate(size={int(size)})

print(json.dumps({{
    "scene": scene.name,
    "report": report,
    "output": str(output)
}}))
"""

        output = self._run_python(code)
        return json.loads(output)
