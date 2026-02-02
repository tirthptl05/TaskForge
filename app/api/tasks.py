from fastapi import APIRouter, HTTPException

from app.core.redis_client import redis
from app.core.task_store import get_task

router = APIRouter()

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "task_id": task_id,
        "task": task
    }
