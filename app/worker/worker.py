from app.core.registry import task_queue, dead_letter_queue, metrics
from app.models.task import Task, TaskStatus
from app.handlers.registry import TASK_HANDLERS
import time


def consume_task() -> Task | None:
    task = task_queue.dequeue()

    if task is None:
        print("Worker: No tasks available")
        return None

    task.status = TaskStatus.PROCESSING
    print("Worker: Processing task")
    print(task)

    try:
        
        handler = TASK_HANDLERS.get(task.type)

        if not handler:
            raise Exception(f"No handler found for task type: {task.type}")

        handler(task)

        task.status = TaskStatus.DONE
        metrics.task_processed()
        print("Worker: Task completed")

    except Exception as e:
        print(f"Worker: Task failed - {e}")

        if task.retries > 0:
            task.retries -= 1
            task.status = TaskStatus.PENDING
            metrics.task_retried()
            print(f"Worker: Retrying task, retries left = {task.retries}")
            task_queue.enqueue(task)
        else:
            task.status = TaskStatus.FAILED
            metrics.task_failed()
            dead_letter_queue.enqueue(task)
            print("Worker: Task moved to Dead Letter Queue")

    return task


def start_worker():
    print("Worker started. Waiting for tasks...")

    while True:
        consume_task()
        time.sleep(2)


