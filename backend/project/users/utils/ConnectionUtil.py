from project.users.models import Connection, User
from datetime import datetime
from project.conversations.utils import ChatUtil
from project.users.utils import UserUtil


def is_connection_object_exists(user, user_connection):
    if Connection.objects.filter(user=user, user_connection=user_connection).exists():
        return True
    return False


def is_already_connected(user, user_connection):
    if Connection.objects.filter(user=user, user_connection=user_connection).exists():
        return True
    elif Connection.objects.filter(user=user_connection, user_connection=user).exists():
        return True
    return False


def check_already_accepted(user_id, user_connection_id):
    if Connection.objects.filter(
        user=user_id, user_connection=user_connection_id, accepted_at__isnull=False
    ).exists():
        raise Exception("Already connected")


def is_pending_connection(user_id, user_connection_id):
    if not Connection.objects.filter(
        user=user_id, user_connection=user_connection_id, accepted_at__isnull=True
    ).exists():
        return False
    return True


def accept_connection_request(user_id, user_connection_id):
    connection = Connection.objects.get(
        user=user_id, user_connection=user_connection_id, accepted_at__isnull=True
    )
    connection.accepted_at = datetime.now()
    connection.save()
    return connection


def accept_connection(user, user_connection_id):
    check_already_accepted(user_connection_id, user.id)
    if not is_pending_connection(user_connection_id, user.id):
        raise Exception("Unable to accept the request")
    connection = accept_connection_request(user_connection_id, user.id)
    ChatUtil.initialize_chat(connection.user, connection.user_connection)
    return connection.user


def ignore_connection(user, user_connection_id):
    if not is_pending_connection(user_connection_id, user.id):
        raise Exception("Unable to ignore the request")
    delete_connection(user_connection_id, user.id)


def delete_connection(user_id, user_connection_id):
    connection = Connection.objects.get(
        user=user_id, user_connection=user_connection_id, accepted_at__isnull=True
    )
    connection.delete()


def get_mutual_paginator(user, user_connection_id):
    mutuals = get_mutuals(user, user_connection_id)
    mutuals = User.objects.filter(id__in=mutuals).order_by("-id")
    return mutuals


def get_mutuals(user, user_connection_id):
    user_accepted_connection = get_accepted_connection(user)
    user_connection_accepted_connection = get_accepted_connection(
        User.objects.get(pk=user_connection_id)
    )
    return user_accepted_connection.intersection(user_connection_accepted_connection)


def get_accepted_connection(user):
    return (
        Connection.objects.filter(user=user, accepted_at__isnull=False)
        .values_list("user_connection", flat=True)
        .union(
            Connection.objects.filter(
                user_connection=user, accepted_at__isnull=False
            ).values_list("user", flat=True)
        )
    )


def check_connection_exist(user, user_connection):
    connection = Connection.objects.filter(user=user, user_connection=user_connection)
    if connection.exists():
        return connection
    connection = Connection.objects.filter(user=user_connection, user_connection=user)
    if connection.exists():
        return connection
    raise Exception("Unable to disconnect")


def disconnect(user, user_connection_id):
    connection = check_connection_exist(user.id, user_connection_id)
    connection.delete()


def cancel_connection(user, user_connection_id):
    if not is_pending_connection(user.id, user_connection_id):
        raise Exception("Unable to cancel the request")
    delete_connection(user.id, user_connection_id)


def get_connection_or_None(user, user_connection):
    connection = Connection.objects.filter(user=user, user_connection=user_connection)
    if connection.exists():
        return connection.first()
    connection = Connection.objects.filter(user_connection=user, user=user_connection)
    if connection.exists():
        return connection.first()
    return None



def get_friends(user):
    friends_ids = get_accepted_connection(user)
    friends = User.objects.filter(id__in=friends_ids)
    return friends


def get_all_connections(user):
    return (
        Connection.objects.filter(user=user)
        .values_list("user_connection", flat=True)
        .union(
            Connection.objects.filter(
                user_connection=user
            ).values_list("user", flat=True)
        )
    )


def get_connections(user_id):
    user = UserUtil.get_user_from_id_or_raise_exception(user_id)
    friends = get_friends(user)
    return friends