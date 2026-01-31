from app.models.task import Task

def handle_email(task: Task) -> None:
    print(f"Sending email with payload: {task.payload}")
