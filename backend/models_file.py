# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthorStarView(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "author_star_views"


class ChatArchive(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    chat = models.ForeignKey("Chat", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chat_archives"


class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    connection = models.ForeignKey("User", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "chats"


class CommentHashtag(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.ForeignKey("Comment", models.DO_NOTHING)
    hashtag = models.ForeignKey("Hashtag", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "comment_hashtag"


class CommentMention(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    comment = models.ForeignKey("Comment", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "comment_mention"


class CommentVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    comment = models.ForeignKey("Comment", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "comment_votes"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    content = models.TextField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "comments"


class Connection(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    connection = models.ForeignKey("User", models.DO_NOTHING)
    message = models.TextField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "connections"


class Favorite(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "favorites"


class Hashtag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "hashtags"


class LastMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    chat = models.ForeignKey(Chat, models.DO_NOTHING)
    message = models.ForeignKey("Message", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "last_messages"


class LinkPreview(models.Model):
    id = models.BigAutoField(primary_key=True)
    previewable_id = models.BigIntegerField()
    previewable_type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "link_previews"


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    chat_id = models.BigIntegerField()
    type = models.CharField(max_length=8)
    content = models.TextField()
    photo_original = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=9)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "messages"


class Migration(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = "migrations"


class Note(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    content = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "notes"


class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    connection = models.ForeignKey("User", models.DO_NOTHING)
    type = models.CharField(max_length=22)
    notifiable_type = models.CharField(max_length=255)
    notifiable_id = models.BigIntegerField()
    is_read = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "notifications"


class PollChoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    poll = models.ForeignKey("Poll", models.DO_NOTHING)
    value = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "poll_choices"


class PollVote(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    poll = models.ForeignKey("Poll", models.DO_NOTHING)
    choice = models.ForeignKey(PollChoice, models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "poll_votes"


class Poll(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey("Post", models.DO_NOTHING, unique=True)
    question = models.CharField(max_length=255)
    end_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "polls"


class PostAlbumPhoto(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    photo = models.CharField(max_length=255)
    photo_original = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "post_album_photos"


class PostContent(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey("Post", models.DO_NOTHING, unique=True)
    type = models.CharField(max_length=8)
    body = models.TextField()
    photo_original = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    cover_original = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "post_contents"


class PostHashtag(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    hashtag = models.ForeignKey(Hashtag, models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "post_hashtag"


class PostMention(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "post_mention"


class PostUnfollow(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    post = models.ForeignKey("Post", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "post_unfollows"


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    team = models.ForeignKey("Team", models.DO_NOTHING)
    caption = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "posts"


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    reportable_id = models.BigIntegerField()
    reportable_type = models.CharField(max_length=255)
    category = models.CharField(max_length=10)
    message = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reports"


class Settings(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    enabled_notification = models.IntegerField()
    is_dark_mode = models.IntegerField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "settings"


class Star(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    post = models.ForeignKey(Post, models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stars"


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    photo = models.CharField(max_length=255)
    goal = models.TextField()
    placeholder = models.TextField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "teams"


class Unfollow(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING)
    connection = models.ForeignKey("User", models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "unfollows"


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=11, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255)
    avatar_original = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    session_at = models.DateTimeField(blank=True, null=True)
    is_online = models.IntegerField()
    email_verified_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"


class Website(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, unique=True)
    personal = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "websites"
