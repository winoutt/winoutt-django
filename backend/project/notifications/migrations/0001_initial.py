# Generated by Django 3.1.2 on 2020-11-01 16:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('notification_type', models.CharField(max_length=22)),
                ('notifiable_id', models.BigIntegerField(blank=True, null=True)),
                ('is_read', models.BooleanField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('notifiable_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_user', to=settings.AUTH_USER_MODEL)),
                ('user_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_user_connection', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]