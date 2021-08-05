from pusher import Pusher
from django.conf import settings

def create_pusher():
    return Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_APP_KEY,
        secret=settings.PUSHER_SECRET,
        cluster=settings.PUSHER_CLUSTER,
    )


def broad_cast_notification(user, message):
    pusher = create_pusher()
    pusher.trigger(u"private-user." + str(user.id), u"notification.created", message)


def broad_cast_message(user_id, status, message):
    pusher = create_pusher()
    pusher.trigger(u"private-user." + str(user_id), u"message." + status, message)


def broad_cast_report_message(message):
    pusher = create_pusher()
    pusher.trigger(u"private-reporting", u"reporting.created", message)


def broad_cast_post_created_message(post, message):
    pusher = create_pusher()
    pusher.trigger(u"private-team." + str(post.team.team_id), u"post.created", message)


def broad_cast_message_created_message(user_id, message):
    pusher = create_pusher()
    pusher.trigger(u"private-user." + str(user_id), u"message.created", message)


def pusher_authentication(channel_name, socket_id, user_id):
    pusher_client = create_pusher()
    auth = pusher_client.authenticate(channel=channel_name, socket_id=socket_id, custom_data=user_id)
    return auth