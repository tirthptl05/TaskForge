from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.models.task import Task
from app.core.registry import task_queue
from app.worker.worker import consume_task



class TaskRequest(BaseModel):
    type: str
    payload: Dict[str, Any]
    retries: int = 3


router = APIRouter()



@router.post("/enqueue")
def enqueue_task(task_request: TaskRequest):

    task = Task(**task_request.model_dump())

    task_queue.enqueue(task)

    return {
        "status": "success",
        "message": "Task successfully enqueued",
        "task_type": task.type
    }




@router.post("/consume-once")
def consume_once():
    task = consume_task()

    if task is None:
        return {
            "status": "empty",
            "message": "No tasks to consume"
        }

    return {
        "status": "processed",
        "task_type": task.type
    }
