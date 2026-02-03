from app.core.redis_client import get_redis_client

class Metrics:
    def __init__(self):
        self.redis = get_redis_client()

    def get_metrics(self):
        return {
            "tasks": {
                "processed": int(self.redis.get("metrics:processed:all") or 0),
                "failed": int(self.redis.get("metrics:failed:all") or 0),
                "retried": int(self.redis.get("metrics:retried:all") or 0),
            },
            "queues": {
                "main_queue_length": self.redis.llen("taskforge:main_queue"),
                "retry_queue_length": self.redis.zcard("retry_queue"),
            }
        }
