# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Model Imports
from .models import Message


# Serializer Imports
from .serializers import MessageSerializer, ChatSerializer

# Utils Imports
from .utils import MessageUtil, ChatUtil, LastMessageUtil, ChatArchiveUtil
from project.posts.utils import LinkPreviewUtil

# Forms Imports
from .forms import MessageForm

# Service Imports
from project.custom_services import MetaDataService, PusherEvents

# Message Views

class Message(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None, *args, **kwargs):        
        try:
            message_form = MessageForm(request.data, request=request)
            if not message_form.is_valid():
                return Response({"message": message_form.errors}, status=status.HTTP_400_BAD_REQUEST)
            message = message_form.save()
            LastMessageUtil.sync_last_message(message.chat, message)
            ChatArchiveUtil.delete_archived_chats(message.chat)
            url = MetaDataService.get_url(message.content)
            if url is not None:
                data = MetaDataService.get_metadata(url)
                LinkPreviewUtil.create(message, data)
            message_receiver = MessageUtil.get_message_receiver(message)
            PusherEvents.broad_cast_message_created_message(message_receiver.id, {"message_id": message.message_id})
        except Exception as error:
            errors = {"error": ["Unable to create message"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(MessageSerializer(message, context={'request': request}).data, status=status.HTTP_201_CREATED)


class ReadMessage(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, message_id, format=None, *args, **kwargs):
        try:
            message = MessageUtil.read_message(request.user, message_id)
            return Response(MessageSerializer(message, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class PaginateMessages(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, chat_id, format=None, *args, **kwargs):
        try:
            messages = MessageUtil.paginate(request.user, chat_id)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(messages, request)
            message_serializer = MessageSerializer(results, many=True, context={'request': request})
            return paginator.get_paginated_response(message_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UnreadMessageCount(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, *args, **kwargs):
        try:
            unreads_message_count = MessageUtil.get_unreads_message_count_from_user(request.user)
            return Response({"unreads_count": unreads_message_count}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to collect unread messages count"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ChatArchiveHandler(APIView):
    permission_classes = [IsAuthenticated]
    
    # UnArchive Chat
    def post(self, request, chat_id, format=None, *args, **kwargs):
        try:
            ChatUtil.unarchive_chat(request.user, chat_id)
            return Response({"isUnarchived": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    # Archive Chat
    def delete(self, request, chat_id, format=None, *args, **kwargs):
        try:
            ChatUtil.archive_chat(request.user, chat_id)
            return Response({"isArchived": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ChatPaginator(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get(self, request, format=None, *args, **kwargs):
        # try:
        chats = ChatUtil.paginate(request.user)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(chats, request)
        chat_serializer = ChatSerializer(results, many=True, context={'request': request})
        return paginator.get_paginated_response(chat_serializer.data)
        # except Exception as error:
        #     errors = {"error": ["Unable to collect chats"]}
        #     return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ArchivedChat(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get(self, request, page=0, format=None, *args, **kwargs):
        try:
            chats = ChatUtil.get_archived_chats(request.user)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(chats, request)
            chat_serializer = ChatSerializer(results, many=True, context={'request': request})
            return paginator.get_paginated_response(chat_serializer.data)
        except Exception as error:
            errors = {"error": ["Unable to collect chats"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SearchChat(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            term = self.request.query_params.get('term')
            chats = ChatUtil.search_chat(request.user, term)
            return Response(ChatSerializer(chats, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to search chats"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)



class ReadChat(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id, format=None, *args, **kwargs):
        try:
            ChatUtil.read_chat_messages(request.user, chat_id)
            return Response({"isRead": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class MarkDelivered(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        try:
            ChatUtil.mark_messages_status_as_delivered(request.user)
            return Response({"isMarkDelivered": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ReadFromUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            chat = ChatUtil.get_chat_from_user(request.user.id, user_id)
            return Response(ChatSerializer(chat, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


