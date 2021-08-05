from project.conversations.models import LastMessage
from datetime import datetime

def get_last_message_or_None(chat):
    last_message = LastMessage.objects.filter(chat=chat)
    if last_message.exists():
        return last_message.first()
    return None

def sync_last_message(chat, message):
    last_message = get_last_message_or_None(chat)
    if last_message is None:
        LastMessage.objects.create(chat=chat, message=message)
    else:
        last_message.message = message
        last_message.updated_at = datetime.now()
        last_message.save()