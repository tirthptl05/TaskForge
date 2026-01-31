class Metrics:
    def __init__(self):
        self.processed = 0
        self.failed = 0
        self.retried = 0

    def task_processed(self):
        self.processed += 1

    def task_failed(self):
        self.failed += 1

    def task_retried(self):
        self.retried += 1
