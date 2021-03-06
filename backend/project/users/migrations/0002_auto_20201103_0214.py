# Generated by Django 3.1.2 on 2020-11-02 21:14

import django.core.files.storage
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enduser',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=None, default='https://winoutt-prod.s3.us-east-2.amazonaws.com/assets/default-avatar.png', force_format=None, keep_meta=True, quality=75, size=[200, 200], storage=django.core.files.storage.FileSystemStorage(location='E:\\Projects\\winoutt-django/winoutt-django/users/static/users/profile_images/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='enduser',
            name='avatar_original',
            field=django_resized.forms.ResizedImageField(crop=None, default='https://winoutt-prod.s3.us-east-2.amazonaws.com/assets/default-avatar.png', force_format=None, keep_meta=True, quality=75, size=[1920, 1080], storage=django.core.files.storage.FileSystemStorage(location='E:\\Projects\\winoutt-django/winoutt-django/users/static/users/profile_images/'), upload_to=''),
        ),
    ]
