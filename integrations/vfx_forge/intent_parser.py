import re


class GraphicsIntentParser:
    """
    Natural-language graphics/VFX requests ko
    structured task me convert karta hai.
    """

    EFFECT_WORDS = {
        "effect",
        "particle",
        "particles",
        "vfx",
        "smoke",
        "energy",
        "fire",
        "spark",
        "explosion",
    }

    def parse(self, request):
        if not request or not str(request).strip():
            raise ValueError("Graphics request cannot be empty.")

        text = str(request).strip()
        lower = text.lower()

        task_type = "design"

        if any(word in lower for word in self.EFFECT_WORDS):
            task_type = "effect"

        design_words = [
            "design",
            "designer",
            "layout",
            "poster",
            "banner",
            "logo",
            "ui",
            "visual design",
        ]

        if any(word in lower for word in design_words):
            task_type = "design"
        elif any(word in lower for word in ["scene", "world", "city"]):
            task_type = "scene"

        if task_type == "effect":
            effect = self._extract_effect(lower)

            return {
                "task_type": "effect",
                "request": text,
                "effect": effect,
            }

        return {
            "task_type": task_type,
            "request": text,
        }

    def _extract_effect(self, text):
        known_effects = [
            "energy",
            "smoke",
            "fire",
            "spark",
            "explosion",
            "particle",
            "particles",
        ]

        for effect in known_effects:
            if re.search(rf"\b{re.escape(effect)}\b", text):
                return effect

        return "custom"
