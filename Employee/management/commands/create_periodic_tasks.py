from django.core.management.base import BaseCommand
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        for task in self.periodic_task_helpers():
            PeriodicTask.objects.update_or_create(**task)

    @staticmethod
    def get_or_create_crontab(**kwargs):
        crontab, _ = CrontabSchedule.objects.get_or_create(**kwargs)
        return crontab

    def periodic_task_helpers(self):
        return [
            {
                "name": "Notify Employee Events Vie Email",
                "defaults": {
                    "task": "Employee.tasks.notify_employee_events_via_email",
                    "start_time": timezone.now(),
                    "crontab": self.get_or_create_crontab(minute="1", hour="0")
                },
            },
        ]
