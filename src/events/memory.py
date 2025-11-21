import asyncio
from typing import Any, Callable, Dict, List
from .base import EventBus

class InMemoryEventBus(EventBus):
    """In-memory implementation of Event Bus for testing and local development"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False
        self.subscribers.clear()

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        if not self.connected:
            raise RuntimeError("Event bus not connected")
            
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                # Execute callbacks asynchronously
                asyncio.create_task(self._safe_execute(callback, message))

    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Any]) -> None:
        if not self.connected:
            raise RuntimeError("Event bus not connected")
            
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    async def _safe_execute(self, callback: Callable, message: Dict[str, Any]):
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(message)
            else:
                callback(message)
        except Exception as e:
            print(f"Error processing event: {e}")
