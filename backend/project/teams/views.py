# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Model Imports
from .models import Team as TeamModel

# Serializer Imports
from .serializers import TeamSerializer
from project.users.serializers import UserSerializer
from project.posts.serializers import PostDetailSerializer

# Utils Imports
from . import utils


class Team(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        teams = TeamModel.objects.all()
        team_serializer = TeamSerializer(teams, many=True)
        return Response(team_serializer.data)


class TopTeam(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        teams = utils.get_top_teams()
        team_serializer = TeamSerializer(teams, many=True)
        return Response(team_serializer.data)


class ReadTeam(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, format=None):
        try:
            team = utils.get_team_from_slug_or_exception(slug)
            team_serializer = TeamSerializer(team)
            return Response(team_serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_404_NOT_FOUND)

class TeamContributers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id, format=None):
        try:
            users = utils.get_contributers(team_id)
            return Response(UserSerializer(users, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class TeamPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id, format=None):
        try:
            posts = utils.get_team_posts(team_id)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(posts, request)
            post_serializer = PostDetailSerializer(results, many=True, context={'request': request })
            return paginator.get_paginated_response(post_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)