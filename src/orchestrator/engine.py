import asyncio
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class WorkflowStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"

class WorkflowEngine:
    """Orchestrator for managing agent workflows"""
    
    def __init__(self):
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.agents: Dict[str, Dict[str, Any]] = {}

    async def register_agent(self, agent_id: str, capabilities: list) -> None:
        """Register a new agent"""
        self.agents[agent_id] = {
            "capabilities": capabilities,
            "status": "ONLINE",
            "last_heartbeat": datetime.utcnow()
        }

    async def create_workflow(self, workflow_type: str, params: Dict[str, Any]) -> str:
        """Create a new workflow instance"""
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            "id": workflow_id,
            "type": workflow_type,
            "status": WorkflowStatus.PENDING,
            "params": params,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return workflow_id

    async def start_workflow(self, workflow_id: str) -> None:
        """Start a workflow execution"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
            
        workflow = self.workflows[workflow_id]
        if workflow["status"] != WorkflowStatus.PENDING:
            raise ValueError(f"Workflow {workflow_id} cannot be started (Status: {workflow['status']})")
            
        workflow["status"] = WorkflowStatus.RUNNING
        workflow["updated_at"] = datetime.utcnow()
        
        # Simulate async execution
        asyncio.create_task(self._execute_workflow(workflow_id))

    async def _execute_workflow(self, workflow_id: str) -> None:
        """Internal method to execute workflow logic"""
        try:
            # Simulate work
            await asyncio.sleep(0.1)
            
            if workflow_id in self.workflows:
                self.workflows[workflow_id]["status"] = WorkflowStatus.COMPLETED
                self.workflows[workflow_id]["updated_at"] = datetime.utcnow()
        except Exception as e:
            if workflow_id in self.workflows:
                self.workflows[workflow_id]["status"] = WorkflowStatus.FAILED
                self.workflows[workflow_id]["error"] = str(e)
                self.workflows[workflow_id]["updated_at"] = datetime.utcnow()

    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get current status of a workflow"""
        if workflow_id in self.workflows:
            return self.workflows[workflow_id]["status"]
        return None
