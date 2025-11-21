import pytest
import asyncio
from src.orchestrator.engine import WorkflowEngine, WorkflowStatus

@pytest.mark.asyncio
async def test_workflow_lifecycle():
    engine = WorkflowEngine()
    
    # Create
    workflow_id = await engine.create_workflow("TEST_TYPE", {"param": "value"})
    assert engine.get_workflow_status(workflow_id) == WorkflowStatus.PENDING
    
    # Start
    await engine.start_workflow(workflow_id)
    assert engine.get_workflow_status(workflow_id) == WorkflowStatus.RUNNING
    
    # Wait for completion
    await asyncio.sleep(0.2)
    assert engine.get_workflow_status(workflow_id) == WorkflowStatus.COMPLETED

@pytest.mark.asyncio
async def test_agent_registration():
    engine = WorkflowEngine()
    await engine.register_agent("agent-1", ["indexing"])
    assert "agent-1" in engine.agents
    assert engine.agents["agent-1"]["status"] == "ONLINE"

@pytest.mark.asyncio
async def test_invalid_workflow_start():
    engine = WorkflowEngine()
    with pytest.raises(ValueError):
        await engine.start_workflow("non-existent-id")
