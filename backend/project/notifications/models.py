# Model Impots
from django.db import models
from project.users.models import Connection, User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Utility Imports
from datetime import datetime


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User, related_name="notification_user", on_delete=models.CASCADE
    )
    user_connection = models.ForeignKey(
        User, related_name="notification_user_connection", on_delete=models.CASCADE
    )

    notification_type = models.CharField(max_length=22)

    notifiable_id = models.BigIntegerField(blank=True, null=True)
    notifiable_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    notifiable = GenericForeignKey('notifiable_type', 'notifiable_id')


    is_read = models.BooleanField()

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
