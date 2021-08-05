# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from project.custom_services.PusherEvents import broad_cast_report_message



# Form Imports
from .forms import ReportForm


class Report(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        try:
            report_form = ReportForm(request.data, request=request)
            if not report_form.is_valid():
                return Response({"message": report_form.errors}, status=status.HTTP_400_BAD_REQUEST)
            report = report_form.save()
            broad_cast_report_message({"reporting_id": report.report_id})
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"isCreated": True}, status=status.HTTP_201_CREATED)
