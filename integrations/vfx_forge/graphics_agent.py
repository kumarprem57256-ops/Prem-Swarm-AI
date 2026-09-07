from .adapter import VFXForgeAdapter
from .intent_parser import GraphicsIntentParser


class GraphicsVFXAgent:
    """
    Prem Swarm AI ka graphics/VFX specialist agent.
    """

    name = "graphics_vfx_agent"

    def __init__(self):
        self.vfx = VFXForgeAdapter()
        self.parser = GraphicsIntentParser()

    def run(self, task_type, request):
        task_type = str(task_type).strip().lower()

        if not request or not str(request).strip():
            raise ValueError("Graphics/VFX request cannot be empty.")

        request = str(request).strip()

        if task_type == "design":
            return {
                "agent": self.name,
                "task_type": task_type,
                "result": self.vfx.create_design(request),
            }

        if task_type == "effect":
            parsed = self.parser.parse(request)
            effect = parsed.get("effect", request)

            return {
                "agent": self.name,
                "task_type": task_type,
                "result": self.vfx.create_effect(effect),
            }

        if task_type == "scene":
            try:
                size = int(request)
            except ValueError:
                raise ValueError(
                    "Scene request must be a numeric size."
                )

            return {
                "agent": self.name,
                "task_type": task_type,
                "result": self.vfx.generate_scene(size),
            }

        raise ValueError(
            f"Unsupported graphics/VFX task type: {task_type}"
        )
