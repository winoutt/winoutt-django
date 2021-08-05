# Models Import
from project.users.models import EndUser, Connection, Setting, Website, User, GENDERS
from project.posts.models import Post

# Library Imports
import re
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import datetime
from project.posts.utils import PostUtil

def get_requested_accepted_connections_count(user_id):
    return Connection.objects.filter(user=user_id).count()


def get_received_accepted_connections_count(user_id):
    return Connection.objects.filter(user_connection=user_id).count()


def get_posts_count(user_id):
    return Post.objects.filter(user=user_id).count()


def get_settings(user_id):
    setting = Setting.objects.filter(user=user_id)
    if setting.exists():
        return setting.first()
    return None


def get_website(user_id):
    website = Website.objects.filter(user=user_id)
    if website.exists():
        return website.first()
    return None


def get_end_user(user_id):
    end_user = EndUser.objects.filter(user=user_id)
    if end_user.exists():
        return end_user.first()
    return None


def split_full_name(full_name):
    full_name = full_name.split(" ", 1)
    return full_name[0], full_name[1]


def is_username_exist(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


def get_users_count():
    return User.objects.count()


def generate_username(full_name):
    # remove all white spaces & conert to lower case
    full_name = full_name.replace(" ", "")
    username = full_name.lower()

    if not is_username_exist(username):
        return username
    return username + str(get_users_count())


def is_valid_username(username):
    if re.match("^[\w-]+$", username) is None:
        return False
    return True


def get_user_name_or_None(email):
    users = User.objects.filter(email=email)
    if users.exists():
        return users.first().username
    else:
        return None


def get_user_or_None(username_or_email, password):
    user = authenticate(username=username_or_email, password=password)
    if user is not None:
        return user
    else:
        username = get_user_name_or_None(username_or_email)
        if username is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                return user
    return None


def is_user_email_verified(user):
    if user.is_active:
        return True
    return False


def get_user_or_raise_exception(email):
    user = User.objects.filter(email=email)
    if user.exists():
        user = user.first()
        if is_user_email_verified(user):
            raise Exception("Already verified")
        else:
            return user
    else:
        raise Exception("Unable to resend verification")


def search_user(term):
    if not term:
        return term
    return User.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term)).exclude(is_superuser=True)


def validate_unique_email(previous_email, new_email):
    if previous_email == new_email:
        return
    if User.objects.filter(email=new_email).exists():
        raise Exception("Email already exist.")


def validate_unique_username(previous_username, new_username):
    if previous_username == new_username:
        return
    if User.objects.filter(username=new_username).exists():
        raise Exception("Username already exist.")


def is_valid_gender(gender):
    if {v: k for k, v in GENDERS}.get(gender) is None:
        return False
    return True


def get_gender_value(gender):
    return {v: k for k, v in GENDERS}.get(gender)


def check_username(user, username):
    if user.username != username:
        raise Exception("Invalid username")


def delete_user(user):
    user.delete()


def update_user_status(user, is_online):
    end_user = get_end_user(user)
    end_user.is_online = is_online
    end_user.save()
    return user


def get_users(users_ids):
    return User.objects.filter(id__in=users_ids)


def get_user_from_id_or_raise_exception(user_id):
    user = User.objects.filter(id=user_id)
    if user.exists():
        return user.first()
    raise Exception("User not found.")


def update_session(user):
    end_user = get_end_user(user)
    end_user.session_at = datetime.now()
    end_user.save()

def read_user(username):
    user = User.objects.filter(username=username)
    if not user.exists():
        raise Exception("User not found.")
    return user.first()

def get_user_posts(username):
    user = read_user(username)
    return PostUtil.paginate(user)

def search_all_user(term, user=None):
    if term is None:
        return None
    users = search_user(term)
    if user is None:
        return users[0:6]
    return users.exclude(id=user.id)[0:6]

def search_user_with_title(title):
    user_ids = EndUser.objects.filter(Q(title__icontains=title)).values_list("user", flat=True)
    return User.objects.filter(id__in=user_ids)

def search_user_with_city(city):
    user_ids = EndUser.objects.filter(Q(city__icontains=city)).values_list("user", flat=True)
    return User.objects.filter(id__in=user_ids)

def search_user_with_bio(bio):
    user_ids = EndUser.objects.filter(Q(bio__icontains=bio)).values_list("user", flat=True)
    return User.objects.filter(id__in=user_ids)


def ban_user(user_id):
    end_user = get_end_user(user_id)
    if end_user.status == "banned":
        raise Exception("Already Blocked.")
    end_user.status = "banned"
    end_user.save()

def unban_user(user_id):
    end_user = get_end_user(user_id)
    if end_user.status == "active":
        raise Exception("Already Active.")
    end_user.status = "active"
    end_user.save()