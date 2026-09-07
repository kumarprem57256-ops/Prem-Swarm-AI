from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class AgentAdapter:
    agent_id: str
    name: str
    agent: Any
    capabilities: set[str] = field(default_factory=set)
    reliability: float = 1.0
    enabled: bool = True

    def can_handle(self, capability: str) -> bool:
        return capability.lower() in {
            c.lower() for c in self.capabilities
        }

    def execute(self, method: str, **kwargs):
        if not self.enabled:
            raise RuntimeError(f"Agent disabled: {self.agent_id}")

        fn: Callable = getattr(self.agent, method, None)

        if fn is None or not callable(fn):
            raise AttributeError(
                f"{self.agent_id} does not implement '{method}'"
            )

        return fn(**kwargs)
