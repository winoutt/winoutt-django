from project.users.models import PeopleUnfollow
from project.users.utils import UserUtil

def is_user_unfollowed(user, user_connection):
    return PeopleUnfollow.objects.filter(
        user=user, user_connection=user_connection
    ).exists()


def create(user, user_connection):
    return PeopleUnfollow.objects.create(user=user, user_connection=user_connection)

def delete(user, user_connection):
    PeopleUnfollow.objects.get(user=user, user_connection=user_connection).delete()

def unfollow_user(user, user_connection_id):
    user_connection = UserUtil.get_user_from_id_or_raise_exception(user_connection_id)
    if is_user_unfollowed(user, user_connection):
        raise Exception("Already unfollowed")
    create(user, user_connection)

def follow_user(user, user_connection_id):
    user_connection = UserUtil.get_user_from_id_or_raise_exception(user_connection_id)
    if not is_user_unfollowed(user, user_connection):
        raise Exception("Already followed")
    delete(user, user_connection)