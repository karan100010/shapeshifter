from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

class EventBus(ABC):
    """Abstract base class for Event Bus implementation"""
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to the message broker"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the message broker"""
        pass

    @abstractmethod
    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a topic"""
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Any]) -> None:
        """Subscribe to a topic with a callback function"""
        pass
