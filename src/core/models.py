from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class WorkflowState(BaseModel):
    workflow_id: str
    status: WorkflowStatus
    current_step: str
    context: Dict[str, Any]
    checkpoints: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
