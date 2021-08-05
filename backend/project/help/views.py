# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django_email_verification import sendConfirm

# Utils Imports
from . import utils

# Serializer Imports
from .serializers import V3Serializer


class Contact(APIView):
    def post(self, request, format=None):
        try:
            v3_serializer = V3Serializer(data=request.data)
            if not v3_serializer.is_valid():
                return Response(v3_serializer.errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            utils.validate_data(request.data)
            utils.send_contact_email(
                request.data["subject"],
                request.data["name"],
                request.data["message"],
                request.data["email"],
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"isSent": True}, status=status.HTTP_200_OK)
