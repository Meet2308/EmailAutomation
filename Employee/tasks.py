from django.template import Template, Context

from EmailAutomation import celery_app
from .models import Employee, EventTemplate, Log, LastExecution
from django.utils import timezone
from django.db.models import Q, Case, When, BooleanField
from .choices import LogType, EventType
from .utils import EmailClient


@celery_app.task()
def notify_employee_events_via_email():
    event_template = {}
    today_date = timezone.now()

    # get employee queryset who have birthday and anniversary today also we have annotated birthday and work_anniversary
    employee = Employee.objects.filter(
        (Q(birthday__day=today_date.day) & Q(birthday__month=today_date.month))
        | (Q(joining_date__day=today_date.day) & Q(joining_date__month=today_date.month) & ~Q(
            joining_date__year=today_date.year))
    ).annotate(
        is_birthday=Case(
            When(Q(birthday__day=today_date.day) & Q(birthday__month=today_date.month), then=True), default=False,
            output_field=BooleanField()
        ),
        is_work_anniversary=Case(
            When(Q(joining_date__day=today_date.day) & Q(joining_date__month=today_date.month) & ~Q(
                joining_date__year=today_date.year), then=True),
            default=False,
            output_field=BooleanField()
        ),
    )

    # if there are not any employee event than we will create
    if not employee.exists():
        Log.objects.create(log_type=LogType.NO_EVENT, message="No Event Found", is_success=True)
        return

    # if there are employee exists who have today any events we will send him/her wishes email
    for employer in employee.iterator(chunk_size=1000):

        # email context to dynamically bind employee details in email
        template_context = {
            "first_name": employer.first_name,
            "last_name": employer.last_name,
            "joining_date": employer.joining_date,
            "total_years": employer.total_year
        }

        # if employee birthday
        if employer.is_birthday:

            # check html template already exists in event template dict if not fetch from database and set in dictionary,
            # so we have to not retrieve email template for any further birthday wishes
            html_template = event_template.get(EventType.BIRTHDAY)
            if not html_template:
                html_template = EventTemplate.objects.get(event_type=EventType.BIRTHDAY).template
                event_template.update({
                    EventType.BIRTHDAY: html_template
                })

            # html body with dynamically bind context
            template = Template(html_template)
            html_body = template.render(Context(template_context))

            # create email client to send email
            email_client = EmailClient(
                subject="Happy Birthday",
                recipient_email=[employer.email],
                html_template=html_template,
                context=template_context
            )
            try:
                email_client.send_mail()
                Log.objects.create(
                    log_type=LogType.WHILE_SENDING_EMAIL,
                    message=html_body,
                    email=employer.email,
                    event_type=EventType.BIRTHDAY,
                    is_success=True
                )
            except Exception as e:
                Log.objects.create(
                    log_type=LogType.WHILE_SENDING_EMAIL,
                    message=html_body,
                    email=employer.email,
                    event_type=EventType.BIRTHDAY,
                    is_success=False,
                    error_message=str(e)
                )

        # if employee work anniversary
        if employer.is_work_anniversary:
            html_template = event_template.get(EventType.WORK_ANNIVERSARY)
            if not html_template:
                html_template = EventTemplate.objects.get(event_type=EventType.WORK_ANNIVERSARY).template
                event_template.update({
                    EventType.WORK_ANNIVERSARY: html_template
                })
            template = Template(html_template)
            html_body = template.render(Context(template_context))

            email_client = EmailClient(
                subject="Happy Anniversary", recipient_email=[employer.email],
                html_template=html_template, context=template_context
            )
            try:
                email_client.send_mail()
                Log.objects.create(
                    log_type=LogType.WHILE_SENDING_EMAIL,
                    message=html_body,
                    email=employer.email,
                    event_type=EventType.WORK_ANNIVERSARY,
                    is_success=True
                )
            except Exception as e:
                Log.objects.create(
                    log_type=LogType.WHILE_SENDING_EMAIL,
                    # message=html_body,
                    email=employer.email,
                    event_type=EventType.WORK_ANNIVERSARY,
                    is_success=False,
                    error_message=str(e)
                )

    LastExecution.objects.create()
