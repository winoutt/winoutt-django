# Library Import
from rest_framework import serializers, fields

# Model Imports
from .models import Team, team_pic_storage_path

# Utils Imports
# from .utils import UserUtil


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("team_id", "name", "slug", "goal", "placeholder", "photo", "deleted_at", "created_at", "updated_at")

    photo = serializers.SerializerMethodField("get_photo")

    def get_photo(self, obj):
        return obj.photo.name