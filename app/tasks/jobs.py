import time

from app.tasks.celery_app import celery_app


@celery_app.task
def send_welcome_email(email: str) -> str:
    return f"Welcome email scheduled for: {email}"


@celery_app.task
def long_running_calculation(value: int) -> int:
    time.sleep(2)
    return value * value
