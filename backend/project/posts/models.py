# Model Impots
from django.db import models
from project.users.models import User
from project.teams.models import Team

# Library Imports
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django_resized import ResizedImageField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Define Path for Storage Fields
post_attached_pic_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR)
    + "/winoutt-django/posts/static/posts/post_attached_images/"
)
post_attached_cover_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR)
    + "/winoutt-django/posts/static/posts/post_attached_covers/"
)
post_attached_file_storage_path = FileSystemStorage(
    location=str(settings.BASE_DIR)
    + "/winoutt-django/posts/static/posts/post_attached_files/"
)

post_content_types = [
    "image",
    "video",
    "audio",
    "document",
    "article",
    "album",
    "poll",
    "text",
]


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    caption = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PostContent(models.Model):
    post_content_id = models.AutoField(primary_key=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    post_content_type = models.CharField(max_length=8)
    body = models.TextField(blank=True, null=True)
    photo_original = ResizedImageField(
        storage=post_attached_pic_storage_path, blank=True, null=True, quality=75
    )
    cover = ResizedImageField(
        storage=post_attached_cover_storage_path,
        blank=True,
        null=True,
        quality=75,
        size=[200, 200],
    )
    cover_original = ResizedImageField(
        storage=post_attached_cover_storage_path, blank=True, null=True, quality=75
    )

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PostMention(models.Model):
    post_mention_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PostUnfollow(models.Model):
    post_unfollow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PostAlbum(models.Model):
    post_album_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = ResizedImageField(
        storage=post_attached_pic_storage_path,
        blank=True,
        null=True,
        quality=75,
        size=[200, 200],
    )
    photo_original = ResizedImageField(
        storage=post_attached_pic_storage_path, blank=True, null=True, quality=75
    )
    filename = models.FileField(
        storage=post_attached_file_storage_path, blank=True, null=True
    )
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class AuthorStarView(models.Model):
    author_star_view_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class CommentMention(models.Model):
    comment_mention_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class CommentVote(models.Model):
    comment_vote_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Hashtag(models.Model):
    hashtag_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PostHashtag(models.Model):
    post_hashtag_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class CommentHashtag(models.Model):
    comment_hashtag_id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Star(models.Model):
    star_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    end_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PollChoice(models.Model):
    poll_choice_id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class PollVote(models.Model):
    poll_vote_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    poll_choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class LinkPreview(models.Model):
    link_preview_id = models.AutoField(primary_key=True)

    previewable_id = models.BigIntegerField(blank=True, null=True)
    previewable_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    previewable = GenericForeignKey("previewable_type", "previewable_id")

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
