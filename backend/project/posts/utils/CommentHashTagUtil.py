from project.posts.models import CommentHashtag, Hashtag
from project.users.models import User

from project.custom_services import MentionService

def create(comment):
    hashtags = MentionService.parse_keyword(comment.content, "#")
    comment_hashtags = []
    for hashtag_name in hashtags:
        hashtag = Hashtag.objects.filter(name=hashtag_name)
        if not hashtag.exists():
            hashtag = Hashtag.objects.create(name=hashtag_name)
        else:
            hashtag = hashtag.first()
        if CommentHashtag.objects.filter(hashtag=hashtag, comment=comment).exists():
            continue
        comment_hashtag = CommentHashtag.objects.create(hashtag=hashtag, comment=comment)
        comment_hashtags.append(comment_hashtag)