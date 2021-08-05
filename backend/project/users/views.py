# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination


from django.http import Http404
from django_email_verification import sendConfirm


# Model Imports
from .models import User

# Serializer Imports
from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    ConnectionSerializer,
    NoteSerializer,
    EditUserSerializer,
    SettingSerializer
)

from project.posts.serializers import PostSerializer, HashtagSerializer, PostDetailSerializer

# Utils Imports
from .utils import UserUtil, ConnectionUtil, NoteUtil, PeopleUnfollowUtil, PeopleYouMayKnowUtil
from project.notifications import utils as NotificationUtil
from project.posts.utils import HashtagUtil, PostUtil

# Forms Imports
from .forms import UserSettingForm, PasswordChangeForm

# User Views
class UserRegister(APIView):
    """
    create new users.
    """

    def post(self, request, format=None):
        user_serializer = CreateUserSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = user_serializer.save()
        sendConfirm(user)
        return Response({"isRegistered": True}, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    """
    Validate and Login users.
    """

    def post(self, request, format=None):
        try:
            email = request.data.get("email", None)
            username = request.data.get("username", None)
            email_or_username = request.data.get("emailOrUsername")
            password = request.data.get("password")
            user = UserUtil.get_user_or_None(email_or_username, password)
            if user is not None:
                if not user.is_active:
                    errors = {"isNotVerified": True, "email": user.email}
                    return Response(errors, status=status.HTTP_200_OK)
                else:
                    end_user = UserUtil.get_end_user(user.id)
                    if end_user.status == "banned":
                        errors = {"error": "Your account has been blocked by an admin."}
                        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
                    token = Token.objects.create(user=user)
                    login_success_data = {
                        "isLoggedIn": True,
                        "token": token.key,
                    }
                    return Response(login_success_data, status=status.HTTP_200_OK)
            else:
                error_msg = 'username' if username else 'email'
                errors = {"error": ["Incorrect " + error_msg + " or password."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            errors = {"error": ["Unable to login user."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"isLogout": True}, status=status.HTTP_200_OK)


class ResendVerificationEmail(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        try:
            user = UserUtil.get_user_or_raise_exception(email)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            sendConfirm(user)
            return Response({"isResent": True}, status=status.HTTP_200_OK)
        except:
            errors = {"error": ["Unable to send verification email."]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# Connection Views
class Connection(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()
        data["user"] = request.user.id
        connection_serializer = ConnectionSerializer(data=data)
        if not connection_serializer.is_valid():
            return Response(
                connection_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        connection = connection_serializer.save()
        NotificationUtil.connection_request(connection.user, connection.user_connection)
        return Response({"isRequested": True}, status=status.HTTP_200_OK)


class AcceptConnection(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        user_connection_id = kwargs.get("id", None)
        try:
            user_connection = ConnectionUtil.accept_connection(
                request.user, user_connection_id
            )
            NotificationUtil.connection_accept(request.user, user_connection)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isAccepted": True}, status=status.HTTP_200_OK)


class IgnoreConnection(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        user_connection_id = kwargs.get("id", None)
        try:
            user_connection = ConnectionUtil.ignore_connection(
                request.user, user_connection_id
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isIgnored": True}, status=status.HTTP_200_OK)


class MutualConnection(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        user_connection_id = kwargs.get("id", None)
        try:
            mutuals = ConnectionUtil.get_mutual_paginator(
                request.user, user_connection_id
            )
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(mutuals, request)
            user_serializer = UserSerializer(results, many=True, context={'request': request})
            return paginator.get_paginated_response(user_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Disconnect(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        user_connection_id = kwargs.get("id", None)
        try:
            ConnectionUtil.disconnect(request.user, user_connection_id)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isDisconnected": True}, status=status.HTTP_200_OK)


class CancelConnection(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        user_connection_id = kwargs.get("id", None)
        try:
            ConnectionUtil.cancel_connection(request.user, user_connection_id)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isCanceled": True}, status=status.HTTP_200_OK)


class ListConnection(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None, *args, **kwargs):
        user_connection_id = kwargs.get("id", None)
        try:
            friends = ConnectionUtil.get_connections(id)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(friends, request)
            user_serializer = UserSerializer(results, many=True, context={'request': request})
            return paginator.get_paginated_response(user_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)



# Note Views


class Note(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        notes = NoteUtil.get_notes(request.user)
        notes_serializer = NoteSerializer(notes, many=True).data
        return Response(notes_serializer, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        note_serializer = NoteSerializer(data=data)
        if not note_serializer.is_valid():
            return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        note = note_serializer.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)


class ArchivedNoteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        notes = NoteUtil.get_archived_notes(request.user)
        notes_serializer = NoteSerializer(notes, many=True).data
        return Response(notes_serializer, status=status.HTTP_200_OK)


class EditNote(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        content = request.data.get("content")
        if content is None or content == "":
            return Response(
                {"message": "Content cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            note = NoteUtil.get_note_or_exception(pk, request.user)
        except Exception as error:
            errors = {"error": ["Unable to update the note."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data["user"] = request.user.id
        note_serializer = NoteSerializer(note, data=data)
        if not note_serializer.is_valid():
            return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        note = note_serializer.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            NoteUtil.force_delete_note(pk, request.user)
        except Exception as error:
            errors = {"error": ["Unable to delete the note."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isDeleted": True}, status=status.HTTP_200_OK)    


class UnArchivedNote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        note_id = kwargs.get("id", None)
        try:
            note = NoteUtil.get_archived_note_or_exception(note_id, request.user)
        except Exception as error:
            errors = {"error": ["Unable to unarchived the note."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        note.undelete()
        return Response({"isUnarchived": True}, status=status.HTTP_200_OK)


class ArchiveNote(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            note = NoteUtil.get_note_or_exception(pk, request.user)
        except Exception as error:
            errors = {"error": ["Unable to archived the note."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        note.delete()
        return Response({"isArchived": True}, status=status.HTTP_200_OK)


class DeleteBlankNotes(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        try:
            NoteUtil.force_delete_blank_note(request.user)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_200_OK)

# People Views

class PeopleMayKnow(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            users = PeopleYouMayKnowUtil.get_people_you_may_know(request.user)
            return Response(UserSerializer(users, many=True, context={'request': request}).data , status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to get people you many know."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class PeopleMayKnowPaginator(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            users = PeopleYouMayKnowUtil.get_people_you_may_know(request.user)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(users, request)
            user_serializer = UserSerializer(results, many=True, context={'request': request})
            return paginator.get_paginated_response(user_serializer.data)
        except Exception as error:
            errors = {"error": ["Unable to get people you many know."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleSearch(APIView):
    
    def get(self, request, format=None, *args, **kwargs):
        term = self.request.query_params.get('term')
        users = UserUtil.search_user(term)
        return Response(UserSerializer(users, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


# User Views

class EditUser(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        try:
            UserUtil.validate_unique_email(request.user.email, request.data['email'])
            UserUtil.validate_unique_username(request.user.username, request.data['username'])
            edit_user_serializer = EditUserSerializer(request.user, data=request.data)
            if not edit_user_serializer.is_valid():
                return Response(edit_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = edit_user_serializer.save()
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)
       

    def post(self, request, format=None):
        username = request.data.get('username')
        try:
            if username is None:
                raise Exception("Username is required.")
            UserUtil.check_username(request.user, username)
            UserUtil.delete_user(request.user)

        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isDeleted": True}, status=status.HTTP_200_OK)


class UpdateUserStatus(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        is_online = request.data.get('is_online')
        try:
            if is_online is None:
                raise Exception("is_online is required.")
            user = UserUtil.update_user_status(request.user, is_online)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)


class ReadUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = UserUtil.read_user(username)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_200_OK)


class ReadUserPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            posts = UserUtil.get_user_posts(username)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(posts, request)
            post_serializer = PostDetailSerializer(results, context={'request': request}, many=True)
            return paginator.get_paginated_response(post_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_404_NOT_FOUND)

# People Unfollow Views
class PeopleUnfollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_connection_id = request.data.get('connectionId')
        try:
            if user_connection_id is None:
                raise Exception("connectionId is required.")
            PeopleUnfollowUtil.unfollow_user(request.user, user_connection_id)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isUnfollowed": True}, status=status.HTTP_200_OK)

    def delete(self, request, user_connection_id, format=None):
        try:
            PeopleUnfollowUtil.follow_user(request.user, user_connection_id)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isFollowed": True}, status=status.HTTP_200_OK)

# Auth User Views
class AuthUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(UserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)

class UpdateSession(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        try:
            UserUtil.update_session(request.user)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isUpdated": True}, status=status.HTTP_200_OK)


class UpdateSetting(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        setting = UserUtil.get_settings(request.user)
        user_setting_form = UserSettingForm(request.data, instance=setting)
        if not user_setting_form.is_valid():
            return Response({"message": user_setting_form.errors}, status=status.HTTP_400_BAD_REQUEST)
        setting = user_setting_form.save()
        return Response(SettingSerializer(setting).data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        password_form = PasswordChangeForm(request.data, instance=request.user)
        if not password_form.is_valid():
            return Response(password_form.errors, status=status.HTTP_400_BAD_REQUEST)
        user = password_form.save()
        return Response({"isUpdated": True}, status=status.HTTP_200_OK)


# Search All Views
class SearchAll(APIView):

    def get(self, request, format=None):
        try:
            term = self.request.query_params.get('term')
            user = request.user if not request.user.is_anonymous else None
            users = UserUtil.search_all_user(term, user)
            hashtags = HashtagUtil.search_hashtag(term)
            posts = PostUtil.search_post(term)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"hashtags": HashtagSerializer(hashtags, many=True).data,
                         "people": UserSerializer(users, many=True, context={'request': request}).data,
                         "posts": PostDetailSerializer(posts, context={'request': request}, many=True).data}, status=status.HTTP_200_OK)