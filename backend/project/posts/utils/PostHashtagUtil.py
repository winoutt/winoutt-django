from project.posts.models import PostHashtag, Hashtag
from project.users.models import User

from project.custom_services import MentionService

def create(post):
    hashtags = MentionService.parse_keyword(post.caption, "#")

    for hashtag_name in hashtags:
        hashtag = Hashtag.objects.filter(name=hashtag_name)
        if not hashtag.exists():
            hashtag = Hashtag.objects.create(name=hashtag_name)
        else:
            hashtag = hashtag.first()
        if PostHashtag.objects.filter(hashtag=hashtag, post=post).exists():
            continue
        PostHashtag.objects.create(hashtag=hashtag, post=post)