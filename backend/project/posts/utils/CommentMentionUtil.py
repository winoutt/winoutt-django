# Model Imports
from project.posts.models import CommentMention
from project.users.models import User

# Utility Imports
from project.posts.utils import PostUtil
from project.users.utils import ConnectionUtil, UserUtil
from django.db.models import Q

# Service Imports
from project.custom_services import MentionService

def create(comment):
    usernames = MentionService.parse_keyword(comment.content, "@")
    comment_mentions = []
    for username in usernames:
        mentioned_user = User.objects.filter(username=username)
        if not mentioned_user.exists():
            continue
        mentioned_user = mentioned_user.first()
        if CommentMention.objects.filter(user=mentioned_user, comment=comment).exists():
            continue
        comment_mention = CommentMention.objects.create(user=mentioned_user, comment=comment)
        comment_mentions.append(comment_mention)
    
    return comment_mentions


def get_user_ids_list_for_suggestion(user, post):
    author = list([post.user.id])
    accepted_connection = list(ConnectionUtil.get_accepted_connection(user))
    post_comments_users = list(PostUtil.get_all_commentees(post).values_list('user', flat=True))
    user_ids = author + accepted_connection + post_comments_users
    return user_ids


def get_mention_suggestions(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    try:
        user_ids = get_user_ids_list_for_suggestion(user, post)
        users = User.objects.filter(id__in=user_ids)[0:20]
        return users
    except Exception as error:
        raise Exception("Unable to suggest users")


def search_mention_suggestions(user, post_id, term):
    post = PostUtil.get_post_or_exception(post_id)
    try:
        user_ids = get_user_ids_list_for_suggestion(user, post)
        users = UserUtil.search_user(term).filter(id__in=user_ids)[0:20]
        return users
    except Exception as error:
        raise Exception("Unable to suggest users")



def get_comment_mention_or_None(comment_mention_id):
    comment_mention = CommentMention.objects.filter(comment_mention_id=comment_mention_id)
    if comment_mention.exists():
        return comment_mention.first()
    return True