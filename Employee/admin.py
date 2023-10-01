from django.contrib import admin
from .models import Employee, EventTemplate, Log, LastExecution


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "birthday", "joining_date")


@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ("event_type",)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("log_type", "email", "event_type", "is_success", "created_at")


@admin.register(LastExecution)
class LastExecutionAdmin(admin.ModelAdmin):
    pass
