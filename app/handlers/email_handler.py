import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from app.models.task import Task


load_dotenv()

def handle_email(task: Task) -> None:
    payload = task.payload

    to_email = payload.get("to")
    subject = payload.get("subject")
    body = payload.get("body")

    if not to_email or not subject or not body:
        raise ValueError("Email task missing required fields")

    smtp_server = os.getenv("GMAIL_SMTP_SERVER")
    smtp_port = int(os.getenv("GMAIL_SMTP_PORT", 587))
    username = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not smtp_server:
        raise RuntimeError("SMTP server not configured")

    if not username or not password:
        raise RuntimeError("SMTP credentials not configured")

    message = EmailMessage()
    message["From"] = username
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(message)

    except Exception as e:
        raise RuntimeError(f"Failed to send email: {str(e)}")
