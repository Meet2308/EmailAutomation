from rest_framework.serializers import ModelSerializer
from .models import Employee, EventTemplate, Log, LastExecution


class EmployeeListSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EventTemplateListSerializer(ModelSerializer):
    class Meta:
        model = EventTemplate
        fields = "__all__"


class LogListSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"


class LastExecutionListSerializer(ModelSerializer):
    class Meta:
        model = LastExecution
        fields = "__all__"
        extra_kwargs = {
            "last_execution_time": {"format": "%d-%m-%Y %H:%M:%S"}
        }
