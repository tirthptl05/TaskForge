from app.models.task import Task
from app.core.redis_client import get_redis_client
import json

class RedisQueue:
    def __init__(self, name: str):
        self.name = name
        self.redis = get_redis_client()

    def enqueue(self, task):
        self.redis.rpush(self.name, json.dumps(task.model_dump()))

    def dequeue(self):
        data = self.redis.lpop(self.name)
        if data:
            return Task(**json.loads(data))
        return None
