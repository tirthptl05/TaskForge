import time
from app.models.task import TaskStatus
from app.core.redis_client import get_redis_client

redis_client = get_redis_client()  # singleton

def _task_key(task_id: str) -> str:
    return f"task:{task_id}"

def create_task(task_id: str, task_type: str, retries_left: int):
    now = int(time.time())
    redis_client.hset(
        _task_key(task_id),
        mapping={
            "status": TaskStatus.PENDING.value,
            "type": task_type,
            "retries_left": retries_left,
            "created_at": now,
            "updated_at": now
        }
    )

def update_task(task_id: str, **fields):
    fields.pop('redis_client', None)
    fields["updated_at"] = int(time.time())
    redis_client.hset(_task_key(task_id), mapping=fields)

def get_task(task_id: str):
    data = redis_client.hgetall(_task_key(task_id))
    if not data:
        return None
    for field in ["retries_left", "created_at", "updated_at"]:
        if field in data:
            data[field] = int(data[field])
    return data
