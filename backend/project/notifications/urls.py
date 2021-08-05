from . import views
from django.urls import path

urlpatterns = [
    path('api/notifications/<int:notification_id>', views.ReadNotification.as_view(), name='read_notification'),
    path('api/notifications/<int:notification_id>/read', views.ReadNotification.as_view(), name='mark_notification_read'),
    path('api/notifications/unreads/count', views.UnReadNotificationsCount.as_view(), name='get_unread_notifications_count'),
    path('api/notifications/paginate', views.NotificationsPaginator.as_view(), name='notifications_paginator'),
    path('api/notifications/connection-requests', views.ConnectionRequestNotification.as_view(), name='connection_request_notification'),
    path('api/notifications/read/all', views.MarkAllReadNotification.as_view(), name='mark_all_notifications_as_read'),
]
