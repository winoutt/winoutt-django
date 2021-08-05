# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import json

# Utility Imports
from project.administration.utils import AnalyticsUtil, ReportsUtil, UsersUtil, PostsUtil, CommentsUtil
from project.reports import utils as ReportUtil
from project.users.utils import UserUtil
from project.posts.utils import PostUtil, CommentUtil
import django.middleware as middleware
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


# Serializer Imports
from project.reports.serializers import ReportSerializer
from project.users.serializers import UserSerializer
from project.posts.serializers import PostSerializer, CommentSerializer, PostDetailSerializer

# Form Imports
from .forms import SendEmailDataForm
from project.users.forms import PasswordChangeForm

# Custom Service Imports
from project.custom_services.PusherEvents import pusher_authentication


# To Allow Only Admins to perform actions
class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


# Analytics Views

class AnalyticsCount(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            counts = AnalyticsUtil.get_count()
            return Response(counts, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to create message"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsCount(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            counts = AnalyticsUtil.get_count()
            return Response(counts, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to calculate analytics"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TopCountries(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            countries = AnalyticsUtil.get_top_countries()
            return Response(countries, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to display countries"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class MonthlyStatistics(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            statistics = AnalyticsUtil.get_monthly_statistics()
            return Response(statistics, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to display statistics"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# Reporting Views

class ReportsList(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            reports = ReportsUtil.get_latest_reports()
            return Response(ReportSerializer(reports, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to display reports"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Report(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, report_id, format=None, *args, **kwargs):        
        try:
            report = ReportUtil.get_report_or_exception(report_id)
            return Response(ReportSerializer(report).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, report_id, format=None, *args, **kwargs):        
        try:
            report = ReportUtil.get_report_or_exception(report_id)
            report.delete()
            return Response({"is_deleted": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, report_id, format=None, *args, **kwargs):        
        try:
            report = ReportUtil.get_report_or_exception(report_id)
            ReportsUtil.approve_report(report)
            report.delete()
            return Response({"is_approved": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Users Views
class UsersList(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            users = UsersUtil.get_users_list()
            return Response(UserSerializer(users, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUsers(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            term = self.request.query_params.get('term')
            users = UsersUtil.search_users(term)
            return Response(UserSerializer(users, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ReadUser(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, user_id, format=None, *args, **kwargs):        
        try:
            user = UserUtil.get_user_from_id_or_raise_exception(user_id)
            return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class BlockUser(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, user_id, format=None, *args, **kwargs):        
        try:
            user = UserUtil.get_user_from_id_or_raise_exception(user_id)
            UserUtil.ban_user(user.id)
            return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UnblockUser(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, user_id, format=None, *args, **kwargs):        
        try:
            user = UserUtil.get_user_from_id_or_raise_exception(user_id)
            UserUtil.unban_user(user.id)
            return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Post Views
class PostsList(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            posts = PostsUtil.get_posts_list()
            return Response(PostDetailSerializer(posts, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SearchPosts(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            term = self.request.query_params.get('term')
            posts = PostsUtil.search_posts(term)
            return Response(PostSerializer(posts, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Post(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, post_id, format=None, *args, **kwargs):        
        try:
            post = PostUtil.get_post_or_exception(post_id)
            return Response(PostDetailSerializer(post).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None, *args, **kwargs):        
        try:
            post = PostUtil.get_post_or_exception(post_id)
            post.delete()
            return Response({"is_deleted": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Comment Views
class CommentsList(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            comments = CommentsUtil.get_comments_list()
            return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SearchComments(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        try:
            term = self.request.query_params.get('term')
            comments = CommentsUtil.search_comments(term)
            return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, comment_id, format=None, *args, **kwargs):        
        try:
            comment = CommentUtil.get_comment_or_exception(comment_id)
            return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, format=None, *args, **kwargs):        
        try:
            comment = CommentUtil.get_comment_or_exception(comment_id)
            comment.delete()
            return Response({"is_deleted": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Admin Views
class SendEmail(APIView):
    permission_classes = [IsSuperUser]
    
    def post(self, request, format=None, *args, **kwargs):        
        try:
            send_email_data_form = SendEmailDataForm(request.data)
            if not send_email_data_form.is_valid():
                return Response(send_email_data_form.errors, status=status.HTTP_400_BAD_REQUEST)
            receivers_count = send_email_data_form.save()
            return Response({"isSent": True, "receiversCount": receivers_count}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": str(error)}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class AuthCheck(APIView):
    permission_classes = [IsSuperUser]
    
    def get(self, request, format=None, *args, **kwargs):        
        return Response({"has_auth": True}, status=status.HTTP_200_OK)


class AuthSocket(APIView):
    permission_classes = [IsSuperUser]
    
    def post(self, request, format=None, *args, **kwargs):
        channel_name = request.data["channel_name"]
        socket_id = request.data["socket_id"]
        auth = pusher_authentication(channel_name, socket_id, request.user.id)
        return Response(auth)


class AdminLogin(APIView):
    """
    Validate and Login users.
    """

    def post(self, request, format=None):
        try:
            email = request.data.get("email", None)
            password = request.data.get("password")
            user = UserUtil.get_user_or_None(email, password)
            if user is not None and user.is_superuser:
                if not user.is_active:
                    errors = {"isNotVerified": True, "email": user.email}
                    return Response(errors, status=status.HTTP_200_OK)
                else:
                    token = Token.objects.create(user=user)
                    login_success_data = {
                        "isLoggedIn": True,
                        "token": token.key,
                    }
                    response = Response(login_success_data, status=status.HTTP_200_OK)

                    return response
            else:
                errors = {"error": ["Incorrect email or password."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            errors = {"error": ["Unable to login user."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAdminPassword(APIView):
    permission_classes = [IsSuperUser]

    def put(self, request, format=None):
        password_form = PasswordChangeForm(request.data, instance=request.user)
        if not password_form.is_valid():
            return Response(password_form.errors, status=status.HTTP_400_BAD_REQUEST)
        user = password_form.save()
        return Response({"isUpdated": True}, status=status.HTTP_200_OK)
