from django.forms import Form, CharField, EmailField
from project.administration.utils import EmailUtil

class SendEmailDataForm(Form):
    to_email = EmailField(required=False)
    subject = CharField(required=True)
    message = CharField(required=True)

    class Meta:
        fields = ("to_email", "subject", "message")

    def save(self, commit=True):
        to_email = self.cleaned_data.get('to_email')
        subject = self.cleaned_data.get('subject')
        message = self.cleaned_data.get('message')
        receivers_count = EmailUtil.send_emails(to_email, subject, message)
        return receivers_count
        
