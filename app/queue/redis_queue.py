from app.models.task import Task
from app.core.redis_client import get_redis_client
import json


class RedisQueue:
    def __init__(self, name: str):
        self.name = name
        self.redis = get_redis_client()

    def enqueue(self, task: Task):
        self.redis.rpush(self.name, json.dumps(task.model_dump()))

    def dequeue(self):
        result = self.redis.blpop(self.name,timeout=1)

        if result is None:
            return None

        _, data = result
        return Task(**json.loads(data))
    
    def peek_all(self):
        data = self.redis.lrange(self.name, 0, -1)
        return [Task(**json.loads(item)) for item in data]

    def size(self):
        return self.redis.llen(self.name)

    def clear(self):
        self.redis.delete(self.name)

