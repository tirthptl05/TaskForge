from typing import Callable, Dict
from app.models.task import Task
from app.handlers.email_handler import handle_email
from app.handlers.sms_handler import handle_sms

TASK_HANDLERS: Dict[str, Callable[[Task], None]] = {
    "email": handle_email,
    "sms": handle_sms,
}
