from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.models.task import Task
from app.queue.simple_queue import SimpleQueue


class TaskRequest(BaseModel):
    type: str
    payload: Dict[str, Any]
    retries: int = 3


router = APIRouter()

task_queue = SimpleQueue()


@router.post("/enqueue")
def enqueue_task(task_request: TaskRequest):

    task = Task(**task_request.model_dump())

    task_queue.enqueue(task)

    return {
        "status": "success",
        "message": "Task successfully enqueued",
        "task_type": task.type
    }
