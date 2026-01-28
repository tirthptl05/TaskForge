from collections import deque
from app.models.task import Task

class SimpleQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, task: Task) -> None:
        self.queue.append(task)

    def dequeue(self) -> Task | None:
        if self.queue:
            return self.queue.popleft()
        return None

    def size(self) -> int:
        return len(self.queue)
