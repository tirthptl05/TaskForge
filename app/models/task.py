from pydantic import BaseModel, Field
from typing import Dict, Any

class Task(BaseModel):
    type: str = Field(..., description='Type of task to execute')
    payload: Dict[str,Any] = Field(..., description='Task-specific data')
    retries: int = Field(..., ge=0, description='Number of retry attempts')