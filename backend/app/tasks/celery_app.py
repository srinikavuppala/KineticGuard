from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "kinetic_guard_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Force Windows to load the task file explicitly
import app.tasks.notification_tasks