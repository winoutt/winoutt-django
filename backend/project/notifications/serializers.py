# Library Import
from rest_framework import serializers, fields
from django.contrib.contenttypes.models import ContentType
from generic_relations.relations import GenericRelatedField


# Model Imports
from .models import Notification
from project.users.models import User
from project.posts.models import CommentMention, Comment, Star, Post, PostMention

# Serializer Imports
from project.users.serializers import UserSerializer, ConnectionUserSerializer
from project.posts.serializers import CommentMentionSerializer, CommentSerializer, StarSerializer, PostDetailSerializer, PostMentionSerializer

# Utils Imports
from . import utils as NotificationUtil
from project.users.utils import PeopleUnfollowUtil, ConnectionUtil, UserUtil
from project.posts.utils import CommentMentionUtil, CommentUtil, StarUtil, PostUtil, PostMentionUtil


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("notification_id", "user", "user_connection", "notification_type", "notifiable_type", "notifiable_id", "is_read", "deleted_at", "created_at", "updated_at", "is_unfollowed", "is_post_unfollowed", "connection", "notifiable")

    is_unfollowed = serializers.SerializerMethodField("get_is_unfollowed")
    is_post_unfollowed = serializers.SerializerMethodField("get_is_post_unfollowed")
    
    connection = serializers.SerializerMethodField("get_connection")

    # notifiable = GenericRelatedField({
    #     User: UserSerializer(),
    #     CommentMention: CommentMentionSerializer(),
    #     Comment: CommentSerializer(),
    #     Star: StarSerializer(),
    # })

    notifiable = serializers.SerializerMethodField("get_notifiable")
    created_at = serializers.SerializerMethodField("get_created_at")

    def get_created_at(self, obj):
        return str(obj.created_at.date()) + " " + str(obj.created_at.time())

    def get_is_unfollowed(self, obj):
        return False

    def get_is_post_unfollowed(self, obj):
        return False
    
    def get_connection(self, obj):
        connection = ConnectionUtil.get_connection_or_None(obj.user, obj.user_connection)
        return ConnectionUserSerializer(obj.user_connection, context={'connection': connection, "request": self.context.get("request", None)}).data

    def get_notifiable(self, obj):
        request = self.context.get("request", None)
        if obj.notifiable_type == ContentType.objects.get_for_model(User):
            try:
                user = UserUtil.get_user_from_id_or_raise_exception(obj.notifiable_id)
                return UserSerializer(user, context={'request': request}).data
            except Exception as error:
                return None
        elif obj.notifiable_type == ContentType.objects.get_for_model(CommentMention):
            comment_mention = CommentMentionUtil.get_comment_mention_or_None(obj.notifiable_id)
            return CommentMentionSerializer(comment_mention, context={'request': request}).data
        elif obj.notifiable_type == ContentType.objects.get_for_model(Comment):
            comment = CommentUtil.get_comment_or_exception(obj.notifiable_id)
            return CommentSerializer(comment, context={'request': request}).data
        elif obj.notifiable_type == ContentType.objects.get_for_model(Star):
            star = StarUtil.get_star_or_None(obj.notifiable_id)
            return StarSerializer(star, context={'request': request}).data
        elif obj.notifiable_type == ContentType.objects.get_for_model(Post):
            try:
                post = PostUtil.get_post_or_exception(obj.notifiable_id)
                return PostDetailSerializer(post, context={'request': request}).data
            except Exception as error:
                return None
        elif obj.notifiable_type == ContentType.objects.get_for_model(PostMention):
            post_mention = PostMentionUtil.get_post_mention_None(obj.notifiable_id)
            return PostMentionSerializer(post_mention, context={'request': request}).data
        return None

    

