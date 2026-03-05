from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "fastapi_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.task_routes = {
    "app.tasks.jobs.send_welcome_email": {"queue": "emails"},
    "app.tasks.jobs.long_running_calculation": {"queue": "default"},
}
