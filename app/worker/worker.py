from app.core.registry import task_queue
from app.models.task import Task, TaskStatus
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
        if task.type == "fail":
            raise Exception("Simulated task failure")

        task.status = TaskStatus.DONE
        print("Worker: Task completed")

    except Exception as e:
        print(f"Worker: Task failed - {e}")

        if task.retries > 0:
            task.retries -= 1
            task.status = TaskStatus.PENDING
            print(f"Worker: Retrying task, retries left = {task.retries}")
            task_queue.enqueue(task)
        else:
            task.status = TaskStatus.FAILED
            print("Worker: Task discarded, no retries left")

    return task


def start_worker():
    print("Worker started. Waiting for tasks...")

    while True:
        consume_task()
        time.sleep(2)
