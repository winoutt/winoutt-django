# Models Imports
from .models import (
    Post,
    Poll,
    AuthorStarView,
    Comment,
    CommentHashtag,
    CommentMention,
    CommentVote,
    Favorite,
    Hashtag,
    PollChoice,
    PollVote,
    PostAlbum,
    PostContent,
    PostHashtag,
    PostMention,
    PostUnfollow,
    Star,
    LinkPreview,
)

# Utility Imports
from django.contrib import admin

admin.site.register(Post)
admin.site.register(PostContent)
admin.site.register(PostMention)
admin.site.register(PostAlbum)
admin.site.register(PostUnfollow)
admin.site.register(Star)

admin.site.register(AuthorStarView)

admin.site.register(Comment)
admin.site.register(CommentMention)
admin.site.register(CommentVote)

admin.site.register(Favorite)

admin.site.register(Hashtag)
admin.site.register(PostHashtag)
admin.site.register(CommentHashtag)

admin.site.register(Poll)
admin.site.register(PollChoice)
admin.site.register(PollVote)

admin.site.register(LinkPreview)
