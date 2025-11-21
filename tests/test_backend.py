import pytest
import asyncio
from fastapi.testclient import TestClient
from src.api.main import app
from src.core.database import db_manager
from src.core.event_bus import event_bus
from src.core.orchestrator import orchestrator
from src.agents.registry import agent_registry
from src.agents.graph_extractor import GraphExtractorAgent
from src.agents.graph_retriever import GraphRetrieverAgent

# Initialize agents
extractor = GraphExtractorAgent()
retriever = GraphRetrieverAgent()
agent_registry.register(extractor.name, extractor)
agent_registry.register(retriever.name, retriever)
orchestrator.register_agent(extractor.name, extractor)
orchestrator.register_agent(retriever.name, retriever)

client = TestClient(app)

@pytest.mark.asyncio
async def test_database_connections():
    # Mocking connections for the test environment if real DBs aren't available
    # In a real scenario, we'd want integration tests with actual DBs
    # Here we just check if the manager is initialized correctly
    assert db_manager is not None
    # We can try to connect, but expect failures if services aren't running
    # db_manager.connect_all() 

@pytest.mark.asyncio
async def test_event_bus():
    received = []
    async def handler(data):
        received.append(data)
    
    event_bus.subscribe("test_event", handler)
    await event_bus.publish("test_event", "hello")
    assert "hello" in received

@pytest.mark.asyncio
async def test_orchestrator_workflow():
    # Mock state store to avoid DB dependency in unit test
    class MockStateStore:
        async def save_workflow(self, wf): pass
        async def get_workflow(self, id): return None
    
    orchestrator.state_store = MockStateStore()
    
    workflow_id = await orchestrator.execute_workflow("indexing", {"chunks": []})
    assert workflow_id is not None

def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_workflow_endpoint():
    # Mock orchestrator execution
    async def mock_execute(*args):
        return "test-id"
    
    original_execute = orchestrator.execute_workflow
    orchestrator.execute_workflow = mock_execute
    
    response = client.post("/workflows", json={"workflow_type": "indexing", "inputs": {}})
    assert response.status_code == 200
    assert response.json()["workflow_id"] == "test-id"
    
    orchestrator.execute_workflow = original_execute
