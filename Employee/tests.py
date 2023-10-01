from django.db import IntegrityError
from django.test import TestCase
from .models import Employee, EventTemplate, Log, LastExecution
from .choices import EventType, LogType
from django.utils import timezone
from .tasks import notify_employee_events_via_email


# Create your tests here.

class EmployeeTestCase(TestCase):
    def setUp(self) -> None:
        self.meet_rathod_employee = Employee.objects.create(
            first_name="meet", last_name="rathod", email="meetrathod@gmail.com", birthday="2000-09-30",
            joining_date="2018-01-30"
        )
        self.adam_john_employee = Employee.objects.create(
            first_name="Adam", last_name="John", email="adamjohn@gmail.com", birthday="1998-09-30",
            joining_date="2018-09-30"
        )

    def test_employee_object_creation(self):
        self.assertEquals(self.meet_rathod_employee.email, "meetrathod@gmail.com")
        self.assertEquals(self.adam_john_employee.email, "adamjohn@gmail.com")

    def test_employee_with_same_email_cannot_be_create(self):
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name="Adam", last_name="John", email="adamjohn@gmail.com", birthday="1998-09-30",
                joining_date="2018-09-30"
            )


class EventTemplateTestCase(TestCase):
    def setUp(self) -> None:
        self.birthday_template = EventTemplate.objects.create(
            event_type=EventType.BIRTHDAY,
            template="""
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Birthday Greeting</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
        }
        .birthday-card {
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .greeting-text {
            font-size: 24px;
            margin-bottom: 20px;
        }
        .name {
            font-weight: bold;
            color: #ff4500;
        }
        .footer-text {
            font-size: 14px;
            color: #888888;
        }
    </style>
</head>
<body>
    <div class="birthday-card">
        <div class="greeting-text">
            Happy Birthday, <span class="name">{{ first_name }} {{ last_name }}</span>!
        </div>
        <div class="message">
            Wishing you a fantastic day filled with joy and laughter. May all your dreams and wishes come true!
        </div>
        <div class="footer-text">
            Best Wishes,<br>
            Your Name
        </div>
    </div>
</body>
</html>
            """
        )
        self.work_anniversary_template = EventTemplate.objects.create(
            event_type=EventType.WORK_ANNIVERSARY,
            template="""
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work Anniversary Greeting</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
        }
        .anniversary-card {
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .greeting-text {
            font-size: 24px;
            margin-bottom: 20px;
        }
        .name {
            font-weight: bold;
            color: #007bff;
        }
        .anniversary-info {
            font-size: 18px;
            margin-bottom: 20px;
        }
        .footer-text {
            font-size: 14px;
            color: #888888;
        }
    </style>
</head>
<body>
    <div class="anniversary-card">
        <div class="greeting-text">
            Congratulations <span class="name">{{ first_name }} {{ last_name }}</span>!
        </div>
        <div class="anniversary-info">
            Today marks your {{ total_years }}-year work anniversary with our company. 
            You joined us on {{ joining_date }} and we appreciate your dedicated service and hard work.
        </div>
        <div class="message">
            Thank you for your contributions, and here's to many more successful years together!
        </div>
        <div class="footer-text">
            Best Wishes,<br>
            Your Name
        </div>
    </div>
</body>
</html>
            """
        )

    def test_same_type_of_template_cannot_be_create(self):
        with self.assertRaises(IntegrityError):
            EventTemplate.objects.create(
                event_type=EventType.WORK_ANNIVERSARY,
                template=""
            )


class LogTestCase(TestCase):
    def setUp(self) -> None:
        self.email_successfully_sent_log = Log.objects.create(
            log_type=LogType.WHILE_SENDING_EMAIL,
            email="meetrathod@gmail.com",
            event_type=EventType.BIRTHDAY,
            is_success=True,
            message="Birthday Wish Email Sent Successfully"
        )
        self.email_failed_sent_log = Log.objects.create(
            log_type=LogType.WHILE_SENDING_EMAIL,
            email="meetrathod@gmail.com",
            event_type=EventType.WORK_ANNIVERSARY,
            is_success=False,
            error_message="email not exists"
        )

    def test_log_object_create(self):
        self.assertEquals(self.email_successfully_sent_log.is_success, True)
        self.assertEquals(self.email_failed_sent_log.is_success, False)


class NotifyEmailEventTestCase(TestCase):
    def setUp(self) -> None:
        # create employee data
        today_date = timezone.now()
        self.meet_rathod_employee = Employee.objects.create(
            first_name="meet", last_name="rathod", email="meetrathod@gmail.com",
            birthday=f"2000-{today_date.month}-{today_date.day}",
            joining_date="2018-01-30"
        )
        self.adam_john_employee = Employee.objects.create(
            first_name="Adam", last_name="John", email="adamjohn@gmail.com", birthday="1998-09-23",
            joining_date=f"2018-{today_date.month}-{today_date.day}"
        )

        # create email template
        self.birthday_template = EventTemplate.objects.create(
            event_type=EventType.BIRTHDAY,
            template="""
                    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Birthday Greeting</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    text-align: center;
                }
                .birthday-card {
                    max-width: 400px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                .greeting-text {
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                .name {
                    font-weight: bold;
                    color: #ff4500;
                }
                .footer-text {
                    font-size: 14px;
                    color: #888888;
                }
            </style>
        </head>
        <body>
            <div class="birthday-card">
                <div class="greeting-text">
                    Happy Birthday, <span class="name">{{ first_name }} {{ last_name }}</span>!
                </div>
                <div class="message">
                    Wishing you a fantastic day filled with joy and laughter. May all your dreams and wishes come true!
                </div>
                <div class="footer-text">
                    Best Wishes,<br>
                    Your Name
                </div>
            </div>
        </body>
        </html>
                    """
        )
        self.work_anniversary_template = EventTemplate.objects.create(
            event_type=EventType.WORK_ANNIVERSARY,
            template="""
                    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Work Anniversary Greeting</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    text-align: center;
                }
                .anniversary-card {
                    max-width: 400px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                .greeting-text {
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                .name {
                    font-weight: bold;
                    color: #007bff;
                }
                .anniversary-info {
                    font-size: 18px;
                    margin-bottom: 20px;
                }
                .footer-text {
                    font-size: 14px;
                    color: #888888;
                }
            </style>
        </head>
        <body>
            <div class="anniversary-card">
                <div class="greeting-text">
                    Congratulations <span class="name">{{ first_name }} {{ last_name }}</span>!
                </div>
                <div class="anniversary-info">
                    Today marks your {{ total_years }}-year work anniversary with our company. 
                    You joined us on {{ joining_date }} and we appreciate your dedicated service and hard work.
                </div>
                <div class="message">
                    Thank you for your contributions, and here's to many more successful years together!
                </div>
                <div class="footer-text">
                    Best Wishes,<br>
                    Your Name
                </div>
            </div>
        </body>
        </html>
                    """
        )

        notify_employee_events_via_email()

    def test_logs_created(self):
        self.assertEquals(Log.objects.count(), 2)
        self.assertEquals(Log.objects.filter(event_type=EventType.BIRTHDAY).count(), 1)
        self.assertEquals(Log.objects.filter(event_type=EventType.WORK_ANNIVERSARY).count(), 1)
        self.assertEquals(Log.objects.filter(log_type=LogType.NO_EVENT).count(), 0)
        self.assertEquals(Log.objects.filter(is_success=False).count(), 0)
        self.assertEquals(LastExecution.objects.count(), 1)
