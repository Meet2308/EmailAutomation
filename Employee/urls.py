from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, LogViewSet, LastExecutionViewSet, EventTemplateViewSet

urlpatterns = []

app_name = "Employee"
router = DefaultRouter()
router.register('employee', viewset=EmployeeViewSet, basename="employee")
router.register('log', viewset=LogViewSet, basename="log")
router.register('event_template', viewset=EventTemplateViewSet, basename="event_template")
router.register('last_execution', viewset=LastExecutionViewSet, basename="last_execution")

urlpatterns += router.urls
