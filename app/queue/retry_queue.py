import time
import json
from app.models.task import Task
from app.core.redis_client import get_redis_client


class RetryQueue:
    def __init__(self, name: str):
        self.name = name
        self.redis = get_redis_client()

    def schedule(self, task: Task, delay_seconds: int):
        retry_at = int(time.time()) + delay_seconds

        self.redis.zadd(
            self.name,
            {json.dumps(task.model_dump()): retry_at}
        )

    def get_due_tasks(self):
        now = int(time.time())

        tasks = self.redis.zrangebyscore(self.name, 0, now)

        if not tasks:
            return []

        self.redis.zremrangebyscore(self.name, 0, now)

        return [Task(**json.loads(task)) for task in tasks]
