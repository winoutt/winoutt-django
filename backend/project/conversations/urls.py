from django.urls import path, re_path
from . import views

urlpatterns = [
    # Message Urls
    path('api/messages', views.Message.as_view(), name='messages'),
    path('api/messages/<int:message_id>', views.ReadMessage.as_view(), name='read_message'),
    path('api/messages/<int:chat_id>/paginate', views.PaginateMessages.as_view(), name='paginate_messages'),
    path('api/messages/unreads/count', views.UnreadMessageCount.as_view(), name='unread_message_count'),

    # Chats Urls
    path('api/chats/<int:chat_id>/archive', views.ChatArchiveHandler.as_view(), name='archive_chat'),
    path('api/chats/<int:chat_id>/unarchive', views.ChatArchiveHandler.as_view(), name='unarchive_chat'),
    path('api/chats/paginate', views.ChatPaginator.as_view(), name='chat_paginator'),
    path('api/chats/archived', views.ArchivedChat.as_view(), name='chat_archived'),
    path('api/chats/search', views.SearchChat.as_view(), name='chat_search'),
    path('api/chats/<int:chat_id>/read', views.ReadChat.as_view(), name='read_chat'),
    path('api/chats/mark/delivered', views.MarkDelivered.as_view(), name='mark_delivered'),
    path('api/chats/user/<int:user_id>', views.ReadFromUser.as_view(), name='read_from_user'),

]