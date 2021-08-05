from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


def validate_data(data):
    if data.get("email") is None:
        raise Exception("Email cannot be empty.")
    elif data.get("name") is None:
        raise Exception("Name cannot be empty.")
    elif data.get("subject") is None:
        raise Exception("Subject cannot be empty.")
    elif data.get("message") is None:
        raise Exception("Message cannot be empty.")
    try:
        validate_email(data.get("email"))
    except ValidationError as e:
        raise Exception(e.message)


def send_contact_email(subject, name, message, email):
    to = settings.EMAIL_HOST_USER
    from_email = settings.EMAIL_HOST_USER

    email_template = get_template("send_contact_email_template.html")
    data = dict({"name": name, "subject": subject, "message": message})
    email_content = email_template.render(data)

    text_content = ""
    headers = {'Reply-To': email}
    email_obj = EmailMultiAlternatives(subject, text_content, from_email, [to], headers=headers)
    email_obj.attach_alternative(email_content, "text/html")
    email_obj.send()

    return
