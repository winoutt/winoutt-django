# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from project.custom_services import PusherEvents


class PusherAuth(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        channel_name = request.data["channel_name"]
        socket_id = request.data["socket_id"]
        pusher_client = PusherEvents.create_pusher()
        auth = pusher_client.authenticate(
            channel=channel_name,
            socket_id=socket_id
        )
        return Response(auth)