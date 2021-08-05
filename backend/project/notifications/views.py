# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.http import Http404

# Utils Imports
from . import utils

# Serializer Imports
from .serializers import NotificationSerializer

class ReadNotification(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, notification_id, format=None):
        try:
            notification = utils.read_notification(request.user, notification_id)
            return Response(NotificationSerializer(notification, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def put(self, request, notification_id, format=None):
        try:
            utils.mark_notification_read(request.user, notification_id)
            return Response({"isRead": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class UnReadNotificationsCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            unreads_count = utils.get_unread_notifications_count(request.user)
            return Response({"unreads_count": unreads_count}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to collect unread notifications count"]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class NotificationsPaginator(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # try:
        notifications = utils.paginate(request.user)
        paginator = PageNumberPagination()
        results = paginator.paginate_queryset(notifications, request)
        notification_serializer = NotificationSerializer(results, many=True, context={'request': request})
        return paginator.get_paginated_response(notification_serializer.data)
        # except Exception as error:
        #     errors = {"error": ["Unable to paginate notification"]}
        #     return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ConnectionRequestNotification(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            notifications = utils.get_connection_request_notifications(request.user)
            return Response(NotificationSerializer(notifications, many=True, context={'request': request}).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to list connection requests notifications"]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class MarkAllReadNotification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            utils.mark_all_notifications_as_read(request.user)
            return Response({"isRead": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": ["Unable to mark all notifications as read."]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)