# Generated by Django 3.1.2 on 2020-11-02 21:14

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='photo',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='E:\\Projects\\winoutt-django/winoutt-django/teams/static/teams/team_images/'), upload_to=''),
        ),
    ]
