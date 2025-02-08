from celery import Celery

from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "celery_tasks",
    broker=f"{CELERY_BROKER_URL}",
    backend=f"{CELERY_RESULT_BACKEND}",
    include=[
        "celery_files.tasks.process_security_json_data"
    ],  # file contaning the celert tasks
)
