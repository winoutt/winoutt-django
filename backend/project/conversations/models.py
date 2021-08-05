# Model Imports
from django.db import models
from project.users.models import User

# Utility Imports
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django_resized import ResizedImageField


# Define Path for Storage Fields
message_attached_pic_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR)
    + "/winoutt-django/conversations/static/conversations/message_attached_images/"
)
message_attached_file_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR)
    + "/winoutt-django/conversations/static/conversations/message_attached_files/"
)

# Define Message Types
message_types = [
    'text',
    'image',
    'video',
    'audio',
    'document'
]


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="chat_user", on_delete=models.CASCADE)
    user_connection = models.ForeignKey(
        User, related_name="chat_user_connection", on_delete=models.CASCADE
    )

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    message_type = models.CharField(max_length=8)
    content = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=9)

    photo_original = ResizedImageField(
        storage=message_attached_pic_storage_path, blank=True, null=True, quality=75
    )

    photo = ResizedImageField(
        storage=message_attached_pic_storage_path, blank=True, null=True, quality=75, size=[200, 200]
    )

    filename = models.TextField(blank=True, null=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class LastMessage(models.Model):
    last_message_id = models.AutoField(primary_key=True)

    chat = models.ForeignKey(Chat, related_name="chats", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class ChatArchive(models.Model):
    chat_archive_id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
