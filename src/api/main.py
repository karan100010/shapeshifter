from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.core.orchestrator import orchestrator
from src.core.models import WorkflowStatus

app = FastAPI(title="ShapeShifter RAG API")

class WorkflowRequest(BaseModel):
    workflow_type: str
    inputs: Dict[str, Any]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/workflows")
async def create_workflow(request: WorkflowRequest):
    try:
        workflow_id = await orchestrator.execute_workflow(
            request.workflow_type, 
            request.inputs
        )
        return {"workflow_id": workflow_id, "status": "initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    workflow = await orchestrator.state_store.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow
