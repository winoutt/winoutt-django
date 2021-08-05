# Model Imports
from django.db import models
from project.users.models import User

# Utility Imports
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


user_reporting_categories = [
        'mimic',
        'fake',
        'rude',
        'explicit',
        'harassment',
        'violent',
        'other'
]

other_reporting_categories = [
        'rude',
        'explicit',
        'harassment',
        'violent',
        'other'
]

reportable_types = ['comment', 'post', 'user']

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    reportable_id = models.BigIntegerField()
    reportable_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    reportable = GenericForeignKey('reportable_type', 'reportable_id')
    
    category = models.CharField(max_length=10)
    message = models.TextField(blank=True, null=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
