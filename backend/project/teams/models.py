# Model Imports
from django.db import models
from project.users.models import EndUser

# Utility Imports
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Define Path for Image Fields
team_pic_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR) + "/winoutt-django/teams/static/teams/team_images/"
)


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    goal = models.TextField()
    placeholder = models.TextField()

    photo = models.ImageField(storage=team_pic_storage_path)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
