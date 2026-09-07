from .graphics_agent import GraphicsVFXAgent


class GraphicsTaskRouter:
    """
    Graphics/VFX requests ko GraphicsVFXAgent tak route karta hai.
    """

    GRAPHICS_KEYWORDS = {
        "graphics",
        "graphic",
        "vfx",
        "visual",
        "design",
        "render",
        "scene",
        "effect",
        "animation",
        "cinematic",
    }

    def __init__(self):
        self.agent = GraphicsVFXAgent()

    def can_handle(self, request):
        text = str(request).lower()
        return any(
            keyword in text
            for keyword in self.GRAPHICS_KEYWORDS
        )

    def classify(self, request):
        text = str(request).lower()

        if any(word in text for word in ["effect", "particle", "smoke", "energy"]):
            return "effect"

        if any(word in text for word in ["scene", "city", "world"]):
            return "scene"

        return "design"

    def route(self, request):
        if not request or not str(request).strip():
            raise ValueError("Request cannot be empty.")

        request = str(request).strip()

        if not self.can_handle(request):
            return {
                "handled": False,
                "agent": None,
                "task_type": None,
                "result": None,
            }

        task_type = self.classify(request)

        # Scene generation currently requires a numeric size.
        if task_type == "scene":
            return {
                "handled": False,
                "agent": self.agent.name,
                "task_type": task_type,
                "error": "Scene generation requires a numeric size.",
            }

        return self.agent.run(
            task_type,
            request,
        )
