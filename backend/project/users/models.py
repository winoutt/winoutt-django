# Model Imports
from django.db import models
from django.contrib.auth.models import User

# Utility Imports
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from softdelete.models import SoftDeleteModel
from django_resized import ResizedImageField


# Define Path for Image Fields
profile_pic_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR) + "/winoutt-django/users/static/users/profile_images/"
)

# Define Enums
MALE = "MA"
FEMALE = "FE"
UNSPECIFIED = "UN"
GENDERS = (
    (MALE, "male"),
    (FEMALE, "female"),
    (UNSPECIFIED, "unspecified"),
)


class EndUser(models.Model):
    end_user_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=255, blank=True, null=True, default="Entrepreneur"
    )
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    gender = models.CharField(max_length=2, choices=GENDERS, null=True, blank=True)

    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    avatar = ResizedImageField(
        storage=profile_pic_storage_path,
        default="https://winoutt-prod.s3.us-east-2.amazonaws.com/assets/default-avatar.png",
        size=[200, 200],
        quality=75
    )
    avatar_original = ResizedImageField(
        storage=profile_pic_storage_path,
        default="https://winoutt-prod.s3.us-east-2.amazonaws.com/assets/default-avatar.png",
        quality=75
    )

    session_at = models.DateTimeField(blank=True, null=True)
    is_online = models.BooleanField(default=False)

    status = models.CharField(default="active", max_length=10)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Connection(models.Model):
    connection_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    user_connection = models.ForeignKey(
        User, related_name="user_connection", on_delete=models.CASCADE
    )

    message = models.TextField(blank=True, null=True)

    accepted_at = models.DateTimeField(blank=True, null=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Note(SoftDeleteModel):
    note_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PeopleUnfollow(models.Model):
    people_unfollow_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User, related_name="unfollow_user", on_delete=models.CASCADE
    )
    user_connection = models.ForeignKey(
        User, related_name="unfollow_user_connection", on_delete=models.CASCADE
    )

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Setting(models.Model):
    setting_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enabled_notification = models.BooleanField(default=True)
    is_dark_mode = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Website(models.Model):
    website_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
