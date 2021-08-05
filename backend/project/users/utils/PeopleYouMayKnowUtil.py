from project.users.models import User, Connection
from project.users.utils import ConnectionUtil, UserUtil, WebsiteUtil
from django.contrib.admin.utils import flatten
import random


def get_friends_of_friends(friends):
    friends_of_friends = User.objects.none()

    for friend in friends:
        friends_of_friend = ConnectionUtil.get_friends(friend)
        friends_of_friends = friends_of_friends | friends_of_friend
    return friends_of_friends


def get_people_with_same_website(user):
    web_site = UserUtil.get_website(user)
    if web_site is not None and web_site.company is not None:
        website_similar_users = WebsiteUtil.get_all_users_similar_company(
            web_site.company
        )
        return website_similar_users
    return User.objects.none()


def get_people_with_same_profile_info(user):
    users = get_people_with_same_website(user)
    end_user = UserUtil.get_end_user(user)
    if end_user is None:
        return users
    if end_user.title is not None and end_user.title != "":
        users = users | UserUtil.search_user_with_title(end_user.title)
    if end_user.city is not None and end_user.city != "":
        users = users | UserUtil.search_user_with_city(end_user.city)
    if end_user.bio is not None and end_user.bio != "":
        users = users | UserUtil.search_user_with_bio(end_user.bio)
    return users


def get_people_you_may_know(user):
    friends = ConnectionUtil.get_friends(user)
    friends_of_friends = get_friends_of_friends(friends)
    users = get_people_with_same_profile_info(user)
    users = users | friends_of_friends
    excluded_ids = flatten([user.id, list(ConnectionUtil.get_all_connections(user))])
    users = users.exclude(id__in=excluded_ids)
    # To Shuffle Queryset
    users = users.order_by("?")
    return users
