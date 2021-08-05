from project.posts.models import PostMention
from project.users.utils import ConnectionUtil, UserUtil
from django.db.models import Q

# Service Imports
from project.custom_services import MentionService
from project.users.models import User


def get_suggestions(user):
    users_ids = ConnectionUtil.get_accepted_connection(user)
    users = UserUtil.get_users(users_ids).order_by("-id")[0:20]
    return users


def get_search_suggestions(user, term):
    if not term:
        return None
    users_ids = ConnectionUtil.get_accepted_connection(user)
    users = UserUtil.get_users(users_ids).filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term)).order_by("-id")[0:20]
    return users


def create(post):
    usernames = MentionService.parse_keyword(post.caption, "@")
    post_mentions = []
    for username in usernames:
        mentioned_user = User.objects.filter(username=username)
        if not mentioned_user.exists():
            continue
        mentioned_user = mentioned_user.first()
        if PostMention.objects.filter(user=mentioned_user, post=post).exists():
            continue
        post_mention = PostMention.objects.create(user=mentioned_user, post=post)
        post_mentions.append(post_mention)
    
    return post_mentions


def get_post_mention_None(post_mention_id):
    post_mention = PostMention.objects.filter(post_mention_id=post_mention_id)
    if post_mention.exists():
        return post_mention.first()
    return None