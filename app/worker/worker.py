from app.core.registry import task_queue, dead_letter_queue, metrics
from app.models.task import Task, TaskStatus
from app.handlers.handler_registry import TASK_HANDLERS
from app.core.redis_client import get_redis_client
from app.core.task_store import update_task
import time

# ✅ create redis client ONCE at module level
redis_client = get_redis_client()


def consume_task() -> Task | None:
    task = task_queue.dequeue()

    if task is None:
        print("Worker: No tasks available")
        return None

    task.status = TaskStatus.PROCESSING
    update_task(
        task_id=task.task_id,
        status=TaskStatus.PROCESSING.value
    )

    print("Worker: Processing task")
    print(task)

    try:
        handler = TASK_HANDLERS.get(task.type)

        if not handler:
            raise Exception(f"No handler found for task type: {task.type}")

        handler(task)

        task.status = TaskStatus.DONE
        update_task(
            task_id=task.task_id,
            status=TaskStatus.DONE.value
        )

        metrics.task_processed()
        print("Worker: Task completed")

    except Exception as e:
        print(f"Worker: Task failed - {e}")

        if task.retries_left > 0:
            task.retries_left -= 1
            task.status = TaskStatus.PENDING

            update_task(
                task_id=task.task_id,
                status=TaskStatus.PENDING.value,
                retries_left=task.retries_left
            )

            metrics.task_retried()
            task_queue.enqueue(task)

        else:
            task.status = TaskStatus.FAILED
            update_task(
                task_id=task.task_id,
                status=TaskStatus.FAILED.value,
                error=str(e)
            )

            metrics.task_failed()
            dead_letter_queue.enqueue(task)

    return task


def start_worker():
    print("Worker started. Waiting for tasks...")
    while True:
        consume_task()
