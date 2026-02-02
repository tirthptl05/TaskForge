import time
import json
from app.core.redis_client import get_redis_client

redis = get_redis_client()

def _log_key(task_id: str) -> str:
    return f"task:logs:{task_id}"

def log_event(task_id: str, event: str, message: str | None = None):
    entry = {
        "ts": int(time.time()),
        "event": event,
        "message": message
    }

    redis.rpush(_log_key(task_id), json.dumps(entry))
