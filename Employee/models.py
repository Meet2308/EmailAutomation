from django.db import models
from .choices import EventType, LogType
from django.utils import timezone


# Create your models here.


class Employee(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    birthday = models.DateField(verbose_name="Birthday Date")
    joining_date = models.DateField(verbose_name="Joining Date")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_year(self):
        today = timezone.now()
        return today.year - self.joining_date.year - (
                (today.month, today.day) < (self.joining_date.month, self.joining_date.day)
        )


class EventTemplate(models.Model):
    event_type = models.CharField(max_length=255, choices=EventType.choices, unique=True, verbose_name="Event Type")
    template = models.TextField(verbose_name="Email Template")

    def __str__(self):
        return f"{self.event_type}"


class Log(models.Model):
    log_type = models.CharField(max_length=255, choices=LogType.choices)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    event_type = models.CharField(
        max_length=255, choices=EventType.choices, null=True, blank=True, verbose_name="Event Type"
    )
    is_success = models.BooleanField(verbose_name="Is Success")
    message = models.TextField(verbose_name="Message")
    error_message = models.TextField(verbose_name="Error Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")


class LastExecution(models.Model):
    last_execution_time = models.DateTimeField(auto_now=True, verbose_name="Last Execution Time")

    def __str__(self):
        return self.last_execution_time
