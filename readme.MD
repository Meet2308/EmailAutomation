# EmailAutomation

## Step To Set up Project

1) create virtual environment with command
   `python3 -m venv venv `
2) activate virtual environment with command
   `source venv/bin/activate`
3) install required package from requirement file in virtual env with command
   `pip install -r requirement.txt`
4) to sent email set **EMAIL_HOST_USER** and **EMAIL_HOST_PASSWORD** in **setting.py**.
5) to create schema from model run command
   `python manage.py migrate`
6) create periodic tasks
   `python manage.py create_periodic_tasks`
7) to start server run command
   `python manage.py runserver`
8) to run test case run command
   `python manage.py test`
9) to start celery commands
   ` celery -A EmailAutomation worker -l INFO`
10) To create data you have to visit django admin panel
11) To see list of endpoint and schema details visit swagger
    `localhost:8000/swagger` ,`localhost:8000/redoc`

## Works Flow and Database Design

### Python Packages Used

- Django
- DjangoRestFramework
- Celery
- CeleryBeat

### Models

1) **Employee** : This model contain information regarding employee like name, email, joining_date,birthday date,etc
2) **EventTemplate**: This model used for stored email template
3) **Log** : This model store log of event success and failure.
4) **LastExecution**: This model have history of email wishing event occurs.

### WorkFlow

I have used celery beat for sending employee event email daily. I have created one celery task which send event email to
employee with dynamic data populating in email template.This task daily trigger at 00:01 A.M. Any failure or success
while sending email are stored in Log.

file_path : `Employee/tasks.py` \
task_name: `notify_employee_events_via_email`

Api are build with DjangoRestFramework. currently, all api endpoint are open and there is no authentication and
permission applied.