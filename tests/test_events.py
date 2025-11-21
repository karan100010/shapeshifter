import pytest
import asyncio
from src.events.memory import InMemoryEventBus

@pytest.mark.asyncio
async def test_event_bus_connection():
    bus = InMemoryEventBus()
    await bus.connect()
    assert bus.connected
    await bus.disconnect()
    assert not bus.connected

@pytest.mark.asyncio
async def test_publish_subscribe():
    bus = InMemoryEventBus()
    await bus.connect()
    
    received_messages = []
    
    async def handler(message):
        received_messages.append(message)
        
    await bus.subscribe("test-topic", handler)
    
    test_msg = {"data": "hello"}
    await bus.publish("test-topic", test_msg)
    
    # Allow async task to complete
    await asyncio.sleep(0.1)
    
    assert len(received_messages) == 1
    assert received_messages[0] == test_msg
    
    await bus.disconnect()

@pytest.mark.asyncio
async def test_publish_not_connected():
    bus = InMemoryEventBus()
    with pytest.raises(RuntimeError):
        await bus.publish("topic", {})
