from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .models import Employee, EventTemplate, Log, LastExecution
from .serializers import EmployeeListSerializer, EventTemplateListSerializer, LogListSerializer, \
    LastExecutionListSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.

class EmployeeViewSet(mixins.ListModelMixin, GenericViewSet):
    model = Employee
    queryset = model.objects.all()
    serializer_class = EmployeeListSerializer


class EventTemplateViewSet(mixins.ListModelMixin, GenericViewSet):
    model = EventTemplate
    queryset = model.objects.all()
    serializer_class = EventTemplateListSerializer


class LogViewSet(mixins.ListModelMixin, GenericViewSet):
    model = Log
    queryset = model.objects.all()
    serializer_class = LogListSerializer


class LastExecutionViewSet(mixins.ListModelMixin, GenericViewSet):
    model = LastExecution
    queryset = model.objects.all()
    serializer_class = LastExecutionListSerializer

    @action(methods=['get'], detail=False)
    def get_last_execution_time(self, request, *args, **kwargs):
        last_execution_time = self.queryset.last()
        return Response(LastExecutionListSerializer(instance=last_execution_time).data)
