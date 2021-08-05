from django.forms import Form, ModelForm, BooleanField, CharField, ValidationError, MultipleChoiceField
from project.conversations.models import Message, message_types


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ('chat', 'message_type', 'content', 'photo_original', 'filename')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(MessageForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        message_type = self.cleaned_data.get('message_type', None)
        content = self.cleaned_data.get('content', None)
        photo_original = self.cleaned_data.get('photo_original', None)

        if message_type is not None and message_type not in message_types:
            raise ValidationError('Invalid message type.')
        elif message_type == "text" and (content is None or content == ""):
            raise ValidationError('Content is required.')
        elif message_type == "image" and photo_original is None:
            raise ValidationError('photo_original is required.')
       

    def save(self, commit=True):
        message = super(MessageForm, self).save(commit=False)
        message.photo = message.photo_original
        message.status = "sent"
        message.user = self.request.user
        message.save()
        return message