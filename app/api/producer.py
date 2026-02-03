from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from uuid import uuid4

from app.models.task import Task
from app.models.task import TaskStatus
from app.core.registry import task_queue
from app.core.redis_client import redis
from app.core.task_store import create_task
from app.worker.worker import consume_task


class TaskRequest(BaseModel):
    type: str
    payload: Dict[str, Any]
    retries: int = 3


router = APIRouter()


@router.post("/enqueue")
def enqueue_task(task_request: TaskRequest):
    

    task_id = str(uuid4())

    task = Task(
        task_id=task_id,
        type=task_request.type,
        payload=task_request.payload,
        retries_left=task_request.retries
    )

    create_task(
        task_id=task_id,
        task_type=task.type,
        retries_left=task.retries_left
    )

    task_queue.enqueue(task)

    return {
        "status": "success",
        "message": "Task successfully enqueued",
        "task_id": task_id,
        "task_status": TaskStatus.PENDING
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
