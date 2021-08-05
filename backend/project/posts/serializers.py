# Library Import
from rest_framework import serializers, fields

# Model Imports
from .models import (
    Comment,
    Post,
    post_content_types,
    CommentMention,
    Star,
    Hashtag,
    PostContent,
    PollChoice,
    Poll,
    Favorite,
    LinkPreview,
    PostAlbum,
    PostMention,
)

# Utils Imports
from .utils import (
    CommentUtil,
    PostUtil,
    PostContentUtil,
    PollUtil,
    PollChoiceUtil,
    StarUtil,
    PollVoteUtil,
    FavoriteUtil,
    LinkPreviewUtil,
    PostAlbumUtil,
    CommentVoteUtil,
)

# Serializer Imports
from project.users.serializers import UserSerializer
from project.teams.serializers import TeamSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        self.fields["post"].error_messages[
            "does_not_exist"
        ] = "Unable to create comment."  # set the custom error message

    def validate(self, data):
        if len(data["content"]) > 500:
            raise serializers.ValidationError(
                "Comment can contain only 500 characters."
            )
        return data

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("team", "user", "content_type", "caption")

        extra_kwargs = {
            "team": {"required": True},
            "user": {"required": True},
        }

    content_type = serializers.CharField(write_only=True, required=True)
    caption = serializers.CharField(write_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super(CreatePostSerializer, self).__init__(*args, **kwargs)
        # self.fields['post'].error_messages['does_not_exist'] = "Unable to create comment." # set the custom error message

    def validate(self, data):
        if data["content_type"] not in post_content_types:
            raise serializers.ValidationError("Please provide a valid content type.")
        if data["content_type"] == "text":
            errors = PostContentUtil.check_text_types(data)
            if len(errors) > 0:
                raise serializers.ValidationError(errors[0])
        return data

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentMentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMention
        fields = (
            "comment_mention_id",
            "user",
            "comment",
            "deleted_at",
            "created_at",
            "updated_at",
        )

    comment = serializers.SerializerMethodField("get_comment")

    def get_comment(self, obj):
        return CommentSerializer(obj.comment).data


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = "__all__"


class PostMentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMention
        fields = "__all__"


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = "__all__"
        depth = 1


class PollChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollChoice
        fields = (
            "poll_choice_id",
            "poll",
            "value",
            "created_at",
            "updated_at",
            "deleted_at",
            "votes_count",
            "is_voted",
        )

    votes_count = serializers.SerializerMethodField("get_votes_count")
    is_voted = serializers.SerializerMethodField("get_is_voted")

    def get_votes_count(self, obj):
        return PollVoteUtil.get_poll_choice_vote_count(obj)

    def get_is_voted(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        poll_vote = PollVoteUtil.is_poll_choice_vote_exist(request.user, obj)
        return poll_vote.exists()


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
            "poll_id",
            "post",
            "question",
            "end_at",
            "deleted_at",
            "created_at",
            "updated_at",
            "choices",
            "is_voted",
        )

    choices = serializers.SerializerMethodField("get_choices")
    is_voted = serializers.SerializerMethodField("get_is_voted")

    def get_choices(self, obj):
        return PollChoiceSerializer(
            PollChoiceUtil.get_poll_choices_or_None(obj),
            many=True,
            context={"request": self.context.get("request", None)},
        ).data

    def get_is_voted(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        poll_vote = PollVoteUtil.is_poll_vote_exist(obj, request.user)
        return poll_vote.exists()


class LinkPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkPreview
        fields = (
            "link_preview_id",
            "title",
            "description",
            "url",
            "image",
            "deleted_at",
            "created_at",
            "updated_at",
        )


class PostAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAlbum
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "post_id",
            "user_id",
            "team_id",
            "caption",
            "deleted_at",
            "created_at",
            "updated_at",
            "content",
            "poll",
            "user",
            "team",
            "stars_count",
            "comments_count",
            "poll_votes_count",
            "is_user",
            "is_favorited",
            "is_starred",
            "link_preview",
            "album",
        )

    content = serializers.SerializerMethodField("get_content")
    poll = serializers.SerializerMethodField("get_poll")
    user_id = serializers.SerializerMethodField("get_user_id")
    team_id = serializers.SerializerMethodField("get_team_id")
    user = serializers.SerializerMethodField("get_user")
    team = serializers.SerializerMethodField("get_team")
    stars_count = serializers.SerializerMethodField("get_stars_count")
    comments_count = serializers.SerializerMethodField("get_comments_count")
    poll_votes_count = serializers.SerializerMethodField("get_poll_votes_count")
    is_user = serializers.SerializerMethodField("get_is_user")
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    is_starred = serializers.SerializerMethodField("get_is_starred")
    link_preview = serializers.SerializerMethodField("get_link_preview")
    album = serializers.SerializerMethodField("get_album")

    created_at = serializers.SerializerMethodField("get_created_at")

    def get_created_at(self, obj):
        return str(obj.created_at.date()) + " " + str(obj.created_at.time())

    def get_user_id(self, obj):
        return obj.user.id

    def get_team_id(self, obj):
        return obj.team.team_id

    def get_content(self, obj):
        post_content = PostContentUtil.get_post_content_or_None(obj)
        if post_content is None:
            return None
        return PostContentSerializer(post_content).data

    def get_poll(self, obj):
        poll = PollUtil.get_poll_or_None(obj)
        if poll is None:
            return None
        return PollSerializer(
            poll, context={"request": self.context.get("request", None)}
        ).data

    def get_user(self, obj):
        return UserSerializer(
            obj.user, context={"request": self.context.get("request", None)}
        ).data

    def get_team(self, obj):
        return TeamSerializer(
            obj.team, context={"request": self.context.get("request", None)}
        ).data

    def get_stars_count(self, obj):
        return StarUtil.get_post_stars_count(obj)

    def get_comments_count(self, obj):
        return CommentUtil.get_post_comments_count(obj)

    def get_poll_votes_count(self, obj):
        return PollVoteUtil.get_post_poll_votes_count(obj)

    def get_is_user(self, obj):
        if self.context.get("request", None) is None:
            return False
        return self.context["request"].user == obj.user

    def get_is_favorited(self, obj):
        if self.context.get("request", None) is None:
            return False
        return FavoriteUtil.is_favorite_post_exist(self.context["request"].user, obj)

    def get_is_starred(self, obj):
        if self.context.get("request", None) is None:
            return False
        return StarUtil.is_start_post_exist(self.context["request"].user, obj)

    def get_link_preview(self, obj):
        if self.context.get("request", None) is None:
            return False
        link_previews = LinkPreviewUtil.get_post_link_preview(obj)
        if not link_previews.exists():
            return None
        return LinkPreviewSerializer(
            link_previews,
            many=True,
            context={"request": self.context.get("request", None)},
        ).data

    def get_album(self, obj):
        album = PostAlbumUtil.get_post_album(obj)
        if not album.exists():
            return None
        return PostAlbumSerializer(album, many=True).data


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "comment_id",
            "user_id",
            "post_id",
            "content",
            "deleted_at",
            "created_at",
            "updated_at",
            "user",
            "post",
            "is_user",
            "is_voted",
            "is_author",
            "votes_count",
        )

    user_id = serializers.SerializerMethodField("get_user_id")
    post_id = serializers.SerializerMethodField("get_post_id")
    user = serializers.SerializerMethodField("get_user")
    post = serializers.SerializerMethodField("get_post")

    is_user = serializers.SerializerMethodField("get_is_user")
    is_voted = serializers.SerializerMethodField("get_is_voted")
    is_author = serializers.SerializerMethodField("get_is_author")
    votes_count = serializers.SerializerMethodField("get_votes_count")

    created_at = serializers.SerializerMethodField("get_created_at")

    def get_created_at(self, obj):
        return str(obj.created_at.date()) + " " + str(obj.created_at.time())

    def get_user_id(self, obj):
        return obj.user.id

    def get_post_id(self, obj):
        return obj.post.post_id

    def get_user(self, obj):
        return UserSerializer(
            obj.user, context={"request": self.context.get("request", None)}
        ).data

    def get_post(self, obj):
        return PostDetailSerializer(
            obj.post, context={"request": self.context.get("request", None)}
        ).data

    def get_is_user(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        if request.user == obj.user:
            return True
        return False

    def get_is_voted(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return CommentVoteUtil.is_comment_vote_exist(request.user, obj)

    def get_is_author(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        if obj.user == obj.post.user:
            return True
        return False

    def get_votes_count(self, obj):
        return CommentVoteUtil.get_comment_votes_count(obj)


class PostCountSerializer(serializers.ModelSerializer):
    stars_count = serializers.IntegerField(source="star_set.count", read_only=True)
    comments_count = serializers.IntegerField(
        source="comment_set.count", read_only=True
    )

    class Meta:
        model = Post
        fields = (
            "post_id",
            "user",
            "team",
            "caption",
            "deleted_at",
            "created_at",
            "updated_at",
            "stars_count",
            "comments_count",
        )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
