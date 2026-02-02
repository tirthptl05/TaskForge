from app.core.registry import task_queue, dead_letter_queue, metrics, retry_queue
from app.models.task import Task, TaskStatus
from app.handlers.handler_registry import TASK_HANDLERS
from app.core.task_store import update_task
from app.core.task_logger import log_event
import time


def pull_retry_tasks():
    tasks = retry_queue.get_due_tasks()

    for task in tasks:
        log_event(task.task_id, "Retry delay elapsed, re-queuing task")
        task_queue.enqueue(task)


def consume_task() -> Task | None:
    task = task_queue.dequeue()

    if task is None:
        return None

    log_event(task.task_id, "Task picked by worker")

    task.status = TaskStatus.PROCESSING
    update_task(
        task_id=task.task_id,
        status=TaskStatus.PROCESSING.value
    )

    try:
        handler = TASK_HANDLERS.get(task.type)

        if not handler:
            raise Exception(f"No handler found for task type: {task.type}")

        log_event(task.task_id, f"Executing handler: {task.type}")
        handler(task)

        task.status = TaskStatus.DONE
        update_task(
            task_id=task.task_id,
            status=TaskStatus.DONE.value
        )

        log_event(task.task_id, "Task completed successfully")
        metrics.task_processed()

    except Exception as e:
        log_event(task.task_id, f"Task failed with error: {str(e)}")

        if task.retries_left > 0:
            task.retries_left -= 1
            task.status = TaskStatus.PENDING

            update_task(
                task_id=task.task_id,
                status=TaskStatus.PENDING.value,
                retries_left=task.retries_left
            )

            retry_queue.schedule(task, delay_seconds=30)
            log_event(
                task.task_id,
                f"Task scheduled for retry in 30s, retries left: {task.retries_left}"
            )

            metrics.task_retried()

        else:
            task.status = TaskStatus.FAILED
            update_task(
                task_id=task.task_id,
                status=TaskStatus.FAILED.value,
                error=str(e)
            )

            dead_letter_queue.enqueue(task)
            log_event(task.task_id, "Task moved to dead letter queue")

            metrics.task_failed()

    return task


def start_worker():
    print("Worker started. Waiting for tasks...")

    while True:
        pull_retry_tasks()
        consume_task()
        time.sleep(1)
