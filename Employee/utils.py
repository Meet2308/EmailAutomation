from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context


class EmailClient:
    """
    Email Client is used to send email. also can send attachment with email.

    NOTE :
    -------
    => Don't use same filename while sending multiple attachment.

    """

    __slots__ = [
        "subject",
        "body",
        "recipient_email",
        "html_template",
        "context",
        "from_email",
    ]

    def __init__(
            self,
            subject: str,
            recipient_email: list,
            html_template: str = None,
            context: dict = None,
            from_email: str = settings.EMAIL_HOST_USER,
    ):
        if not isinstance(subject, str):
            raise TypeError('"subject" argument must be a str')

        if html_template and not isinstance(html_template, str):
            raise TypeError('"text_template_path" argument must be a str')

        if not isinstance(recipient_email, list):
            raise TypeError('"recipient_email" argument must be a list')

        if not isinstance(from_email, str):
            raise TypeError('"from_email" argument must be a str')

        if context and not isinstance(context, dict):
            raise TypeError('"context" argument must be a dictionary')

        self.subject = subject
        self.html_template = html_template
        self.context = context
        self.from_email = from_email
        self.recipient_email = recipient_email

    def send_mail(self):
        """
        To sent email
        """
        template = Template(self.html_template)
        html_template_with_context = template.render(Context(self.context))

        # html_template_with_context = self.html_template.format(**self.context)
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=html_template_with_context,
            from_email=settings.EMAIL_HOST_USER,
            to=self.recipient_email,
        )
        email.content_subtype = 'html'

        email.send(fail_silently=False)
