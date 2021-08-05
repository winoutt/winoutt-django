from project.posts.models import Hashtag, Post, PostHashtag
from django.db.models import Count, Q

def get_trending_hashtags():
    return Hashtag.objects.annotate(post_count=Count("posthashtag")).order_by("-post_count")[0:5]

def get_hashtag_from_name_or_exception(hashtag):
    hashtag = Hashtag.objects.filter(name=hashtag)
    if hashtag.exists():
        return hashtag.first()
    raise Exception("Hashtag not found")

def get_posts(hashtag):
    hashtag = get_hashtag_from_name_or_exception(hashtag)
    post_ids = PostHashtag.objects.filter(hashtag=hashtag).values_list('post', flat=True)
    return Post.objects.filter(post_id__in=post_ids).order_by("-post_id")

def search_hashtag(term):
    if term is None:
        return None
    hashtags = Hashtag.objects.filter(Q(name__icontains=term))[0:5]
    return hashtags