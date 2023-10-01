import os

import celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EmailAutomation.settings")

celery_app = celery.Celery("EmailAutomation")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
