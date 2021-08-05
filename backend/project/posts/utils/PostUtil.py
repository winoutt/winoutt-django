from project.posts.models import Post
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q

def get_all_commentees(post):
    commentees = post.comment_set.all().values('user').distinct()
    return commentees


def get_post_or_exception(post_id):
    post = Post.objects.filter(post_id=post_id)
    if post.exists():
        return post.first()
    raise Exception("Unable to find the post")


def get_post_or_exception_on_user(post_id, user):
    post = Post.objects.filter(post_id=post_id, user=user)
    if post.exists():
        return post.first()
    raise Exception("Unable to find the post")


def paginate(user):
    return Post.objects.filter(user=user).order_by("-post_id")


def get_top_posts():
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gt=some_day_last_week).annotate(stars_count=Count("star", distinct=True),
            comments_count=Count("comment", distinct=True)
            ).order_by('-stars_count', '-comments_count')
    return posts


def search_post(term):
    if term is None:
        return None
    posts = Post.objects.filter(Q(caption__icontains=term))[0:5]
    return posts


def get_posts_from_ids(post_ids):
    return Post.objects.filter(post_id__in=post_ids)