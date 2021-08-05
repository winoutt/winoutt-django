from project.administration.utils import UsersUtil
import threading


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

def send_email_thread(email_obj):
    email_obj.send()


def send_emails(to_email, subject, message):
    receivers = [to_email] if to_email != "" else list(UsersUtil.get_emails())

    from_email = settings.EMAIL_HOST_USER

    email_template = get_template("broad_cast_email_from_admin.html")
    data = dict({"name": "abc", "subject": subject, "message": message})
    email_content = email_template.render(data)

    text_content = ""
    email_obj = EmailMultiAlternatives(subject, text_content, from_email, receivers)
    email_obj.attach_alternative(email_content, "text/html")
    
    thread = threading.Thread(target=send_email_thread,args=[email_obj],daemon=True)
    thread.start()

    return len(receivers)

    