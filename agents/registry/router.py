class AgentRouter:
    def __init__(self, registry):
        self.registry = registry

    def route(self, capability: str):
        candidates = self.registry.find_by_capability(capability)

        if not candidates:
            raise LookupError(
                f"No enabled agent found for capability: {capability}"
            )

        # V1: highest reliability wins
        candidates.sort(
            key=lambda agent: agent.reliability,
            reverse=True
        )

        return candidates[0]

    def route_many(self, capabilities):
        return {
            capability: self.route(capability)
            for capability in capabilities
        }
