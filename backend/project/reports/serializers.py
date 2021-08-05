# Library Import
from rest_framework import serializers, fields
from generic_relations.relations import GenericRelatedField


# Model Imports
from project.reports.models import Report
from project.users.models import User
from project.posts.models import Post, Comment

# Serializer Imports
from project.users.serializers import UserSerializer
from project.posts.serializers import PostSerializer, CommentSerializer

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("report_id", "user", "reportable_id", "reportable_type", "reportable", "category", "message", "deleted_at", "created_at", "updated_at") 

    reportable = GenericRelatedField({
        User: UserSerializer(),
        Comment: CommentSerializer(),
        Post: PostSerializer(),
    })