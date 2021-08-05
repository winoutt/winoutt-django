from project.users.models import Setting


def is_notification_enabled(user):
    settings = Setting.objects.filter(user=user)
    if settings.exists():
        return settings.first().enabled_notification
    return False
