# Library Import
from rest_framework import serializers, fields

# Model Imports
from .models import Message, message_types, Chat, LastMessage

# Utils Imports
from project.users.utils import ConnectionUtil
from project.conversations.utils import LastMessageUtil, ChatArchiveUtil, MessageUtil
from project.posts.utils import LinkPreviewUtil


# Serializer imports
from project.users.serializers import  ConnectionSerializer, UserSerializer
from project.posts.serializers import LinkPreviewSerializer

# Message Serailizers



class LastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastMessage
        fields = ('last_message_id', 'chat', 'message', 'deleted_at', 'created_at', 'updated_at', 'content', 'message_type')
    
    content = serializers.SerializerMethodField('get_content')
    message_type = serializers.SerializerMethodField('get_message_type')

    created_at = serializers.SerializerMethodField("get_created_at")

    def get_created_at(self, obj):
        return str(obj.created_at.date()) + " " + str(obj.created_at.time())

    def get_content(self, obj):
        return obj.message.content

    def get_message_type(self, obj):
        return obj.message.message_type



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('chat_id', 'user', 'deleted_at', 'created_at', 'updated_at', 'pivot', 'unreads_count', 'last_message', 'is_archived')

    user = serializers.SerializerMethodField("get_user")
    pivot = serializers.SerializerMethodField("get_pivot")
    unreads_count = serializers.SerializerMethodField("get_unreads_count")
    last_message = serializers.SerializerMethodField("get_last_message")
    is_archived = serializers.SerializerMethodField("get_is_archived")

    created_at = serializers.SerializerMethodField("get_created_at")

    def get_is_archived(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return ChatArchiveUtil.is_exist(request.user, obj)

    def get_created_at(self, obj):
        return str(obj.created_at.date()) + " " + str(obj.created_at.time())

    def get_user(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return None
        user = None
        if request.user == obj.user:
            user = obj.user_connection
        else:
            user = obj.user 
        return UserSerializer(user, context={'request': self.context.get("request", None)}).data

    def get_pivot(self, obj):
        try:
            connection = ConnectionUtil.check_connection_exist(obj.user, obj.user_connection)
            return ConnectionSerializer(connection.first(), context={'request': self.context.get("request", None)}).data
        except Exception as error:
            return None


    def get_unreads_count(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return 0
        return MessageUtil.get_unreads_message_count([obj.chat_id], request.user)


    def get_last_message(self, obj):
        last_message = LastMessageUtil.get_last_message_or_None(obj)
        if last_message is None:
            return None
        return  LastMessageSerializer(last_message).data




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_id', 'chat', 'is_sent', 'chat_id', 'content', 'deleted_at', 'created_at', 'updated_at', 
                'status', 'message_type', 'user', 'filename', 'link_preview')

    chat = serializers.SerializerMethodField("get_chat")
    is_sent = serializers.SerializerMethodField("get_is_sent")
    chat_id = serializers.SerializerMethodField("get_chat_id")
    link_preview = serializers.SerializerMethodField("get_link_preview")

    created_at = serializers.SerializerMethodField("get_created_at")

    def get_created_at(self, obj):
        return str(obj.created_at.date()) + " " + str(obj.created_at.time())

    def get_chat(self, obj):
        return ChatSerializer(obj.chat, context={'request': self.context.get('request', None)}).data

    def get_is_sent(self, obj):
        request = self.context.get('request', None)
        if request is None or request.user != obj.user:
            return False
        return True

    def get_chat_id(self, obj):
        return obj.chat.chat_id

    def get_link_preview(self, obj):
        if self.context.get("request", None) is None:
            return False
        link_previews = LinkPreviewUtil.get_message_link_preview(obj)
        if not link_previews.exists():
            return None
        return LinkPreviewSerializer(link_previews, many=True, context={'request': self.context.get("request", None) }).data