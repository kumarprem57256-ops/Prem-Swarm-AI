from .adapter import AgentAdapter


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, AgentAdapter] = {}

    def register(self, adapter: AgentAdapter):
        if adapter.agent_id in self._agents:
            raise ValueError(
                f"Agent already registered: {adapter.agent_id}"
            )

        self._agents[adapter.agent_id] = adapter
        return adapter

    def unregister(self, agent_id: str):
        return self._agents.pop(agent_id, None)

    def get(self, agent_id: str):
        return self._agents.get(agent_id)

    def all(self):
        return list(self._agents.values())

    def find_by_capability(self, capability: str):
        return [
            agent
            for agent in self._agents.values()
            if agent.enabled and agent.can_handle(capability)
        ]

    def enable(self, agent_id: str):
        agent = self.get(agent_id)
        if agent:
            agent.enabled = True

    def disable(self, agent_id: str):
        agent = self.get(agent_id)
        if agent:
            agent.enabled = False
