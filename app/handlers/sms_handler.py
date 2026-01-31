from app.models.task import Task

def handle_sms(task: Task) -> None:
    print(f"Sending SMS with payload: {task.payload}")
