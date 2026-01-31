from app.queue.redis_queue import RedisQueue
from app.core.metrics import Metrics

task_queue = RedisQueue("taskforge:main_queue")
dead_letter_queue = RedisQueue("taskforge:dead_letter_queue")

metrics = Metrics()