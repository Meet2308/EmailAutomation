class EventType:
    BIRTHDAY = "birthday"
    WORK_ANNIVERSARY = "work_anniversary"

    choices = (
        (BIRTHDAY, "Birthday"),
        (WORK_ANNIVERSARY, "Work Anniversary ")
    )


class LogType:
    WHILE_SENDING_EMAIL = "while_sending_email"
    NO_EVENT = "no_event"
    choices = (
        (WHILE_SENDING_EMAIL, "While Sending Email"),
        (NO_EVENT, "No Event")
    )
