# Model Imports
from project.notifications.models import Notification
from project.users.models import User
from project.posts.models import CommentMention, Comment, CommentVote, Post, PostMention, Star

# Utility Imports
from project.users.utils import UserUtil, PeopleUnfollowUtil, SettingUtil, ConnectionUtil
from project.posts.utils import PostUnfollowUtil, PostUtil, StarUtil
from project.custom_services.PusherEvents import broad_cast_notification

# Library Imports
from pusher import Pusher
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType


def get_notification_or_exception(user, notification_id):
    notification = Notification.objects.filter(notification_id=notification_id, user=user)
    if notification.exists():
        return notification.first()
    notification = Notification.objects.filter(notification_id=notification_id, user_connection=user)
    if notification.exists():
        return notification.first()
    raise Exception("Notification not found")


def can_send_notification(user, user_connection, notification_type, post=None):
    is_same_user = user.id == user_connection.id
    is_enabled = SettingUtil.is_notification_enabled(user_connection)
    is_post_unfollowed = post and PostUnfollowUtil.is_post_unfollowed(user_connection, post)

    is_user_unfollowed = PeopleUnfollowUtil.is_user_unfollowed(user_connection, user)
    
    can_normal = (
        not is_same_user
        and is_enabled
        and not is_post_unfollowed
        and not is_user_unfollowed
    )
    can_request = not is_same_user
    is_connection_request = (notification_type == 'connection_request')
    return can_request if is_connection_request else can_normal


def create_notification(notification_type, user, user_connection, notifiable):
    return Notification.objects.create(user=user, user_connection=user_connection, notification_type=notification_type, is_read=False, notifiable=notifiable)


def connection_request(user, user_connection):
    notification_type = 'connection_request'
    if not can_send_notification(user, user_connection, notification_type): 
        return
    notification = create_notification(notification_type, user_connection, user, user_connection)
    broad_cast_notification(user_connection, {'notification_id': notification.notification_id})


def connection_accept(user, user_connection):
    notification_type = 'connection_accept'
    if not can_send_notification(user, user_connection, notification_type):
        return
    notification = create_notification(notification_type, user_connection, user, user_connection)
    broad_cast_notification(user_connection, {'notification_id': notification.notification_id})


def send_notification_to_comment_mentions(user, comment_mentions):
    for comment_mention_obj in comment_mentions:
        comment_mention(user, comment_mention_obj)


def comment_mention(user, comment_mention):
    notification_type = 'comment_mention'
    if not can_send_notification(user, comment_mention.user, notification_type, comment_mention.comment.post):
        return
    notification = create_notification(notification_type, comment_mention.user, user, comment_mention)
    broad_cast_notification(comment_mention.user, {'notification_id': notification.notification_id})
   

def send_comment_notification_to_user(user, comment):
    notification_type = 'comment'
    if not can_send_notification(user, comment.post.user, notification_type, comment.post):
        return
    notification = create_notification(notification_type, comment.post.user, user, comment)
    broad_cast_notification(comment.post.user, {'notification_id': notification.notification_id})


def send_notification_to_commentee(user, post_comment_user, comment):
    notification_type = 'comment_commented_post'
    if not can_send_notification(user, post_comment_user, notification_type, comment.post):
        return
    notification = create_notification(notification_type, post_comment_user, user, comment)
    broad_cast_notification(post_comment_user, {'notification_id': notification.notification_id})


def send_notification_to_all_commentees(user, comment):
    commentees = PostUtil.get_all_commentees(comment.post)
    for commentee in commentees:
        send_notification_to_commentee(user, User.objects.get(pk=commentee['user']), comment)


def send_notification_to_comment_owner_on_upvote(user, comment):
    notification_type = 'comment_vote'
    if not can_send_notification(user, comment.user, notification_type, comment.post):
        return
    notification = create_notification(notification_type, comment.user, user, comment)
    broad_cast_notification(comment.user, {'notification_id': notification.notification_id})


def send_star_notification_to_user(user, star):
    notification_type = 'star'
    if not can_send_notification(user, star.post.user, notification_type, star.post):
        return
    notification = create_notification(notification_type, star.post.user, user, star)
    broad_cast_notification(star.post.user, {'notification_id': notification.notification_id})


def read_notification(user, notification_id):
    notification = get_notification_or_exception(user, notification_id)
    return notification


def mark_notification_read(user, notification_id):
    notification = get_notification_or_exception(user, notification_id)
    notification.is_read = True
    notification.save()


def get_unread_notifications_count(user):
    unreads_count = Notification.objects.filter(is_read=False, user=user).count()
    return unreads_count


def paginate(user):
    notifiable_types = [ContentType.objects.get_for_model(User), ContentType.objects.get_for_model(CommentMention), ContentType.objects.get_for_model(Comment), ContentType.objects.get_for_model(CommentVote), ContentType.objects.get_for_model(Post), ContentType.objects.get_for_model(PostMention), ContentType.objects.get_for_model(Star)]
    notifications = Notification.objects.filter(notifiable_type__in=notifiable_types, user=user).exclude(notification_type="connection_request").order_by('-notification_id')
    return notifications


def get_connection_request_notifications(user):
    notifications = Notification.objects.filter(notification_type="connection_request", user=user).order_by('-notification_id')[0:20]
    notification_ids = []
    for notification in notifications:
        connection = ConnectionUtil.get_connection_or_None(notification.user, notification.user_connection)
        if connection is None:
            notification_ids.append(notification.notification_id)
            continue
        if connection.accepted_at: 
            is_connected = True
        else:
            is_connected = False
        if connection.user == user:
            is_received = False
        else:
            is_received = True
        is_pending_connection = not is_connected and is_received
        if is_connected or not is_pending_connection:
            notification_ids.append(notification.notification_id)
    notifications = Notification.objects.filter(notification_type="connection_request", user=user).exclude(notification_id__in=notification_ids).order_by('-notification_id')[0:20]
    return notifications


def send_create_post_notification(post):
    notification_type = 'post_create'
    friends = ConnectionUtil.get_friends(post.user)
    for friend in friends:
        if not can_send_notification(post.user, friend, notification_type):
            continue
        else:
            notification = create_notification(notification_type, friend, post.user, post)
            broad_cast_notification(friend, {'notification_id': notification.notification_id})


def send_post_mention_notification(user, post_mention):
    notification_type = 'post_mention'
    if not can_send_notification(user, post_mention.user, notification_type, post_mention.post):
        return
    notification = create_notification(notification_type, post_mention.user, user, post_mention)
    broad_cast_notification(post_mention.user, {'notification_id': notification.notification_id})


def send_comment_notification_to_post_stared_users(user, comment):
    notification_type = 'comment_starred_post'
    post_starred_users = StarUtil.get_stared_post_users(comment.post)
    for post_starred_user in post_starred_users:
        if not can_send_notification(user, post_starred_user, notification_type, comment.post):
            continue
        else:
            notification = create_notification(notification_type, post_starred_user, user, comment.post)
            broad_cast_notification(post_starred_user, {'notification_id': notification.notification_id})


def mark_all_notifications_as_read(user):
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)