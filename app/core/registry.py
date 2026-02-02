from app.queue.redis_queue import RedisQueue
from app.core.metrics import Metrics
from app.queue.retry_queue import RetryQueue

retry_queue = RetryQueue("retry_queue")


task_queue = RedisQueue("taskforge:main_queue")
dead_letter_queue = RedisQueue("taskforge:dead_letter_queue")

metrics = Metrics()