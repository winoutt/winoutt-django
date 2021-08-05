# Generated by Django 3.1.2 on 2020-11-02 21:14

import django.core.files.storage
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=75, size=[200, 200], storage=django.core.files.storage.FileSystemStorage(location='E:\\Projects\\winoutt-django/winoutt-django/conversations/static/conversations/message_attached_images/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='message',
            name='photo_original',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=75, size=[1920, 1080], storage=django.core.files.storage.FileSystemStorage(location='E:\\Projects\\winoutt-django/winoutt-django/conversations/static/conversations/message_attached_images/'), upload_to=''),
        ),
    ]
