from . import views
from django.urls import path

urlpatterns = [
    path('api/reportings', views.Report.as_view(), name='create_report'),
]
