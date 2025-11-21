from typing import Dict, Type
from src.agents.base import BaseAgent

class AgentRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance.agents: Dict[str, BaseAgent] = {}
        return cls._instance

    def register(self, name: str, agent: BaseAgent):
        self.agents[name] = agent

    def get(self, name: str) -> BaseAgent:
        return self.agents.get(name)

agent_registry = AgentRegistry()
