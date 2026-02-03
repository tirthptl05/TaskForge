from app.queue.redis_queue import RedisQueue
from app.core.metrics import Metrics
from app.queue.retry_queue import RetryQueue




task_queue = RedisQueue("taskforge:main_queue")
dead_letter_queue = RedisQueue("taskforge:dead_letter_queue")
retry_queue = RetryQueue("retry_queue")

metrics = Metrics()