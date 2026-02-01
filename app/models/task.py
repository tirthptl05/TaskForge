from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"

class Task(BaseModel):
    task_id: str
    type: str = Field(..., description='Type of task to execute')
    payload: Dict[str,Any] = Field(..., description='Task-specific data')
    retries_left: int = Field(..., ge=0, description='Number of retry attempts')
    status: TaskStatus = TaskStatus.PENDING