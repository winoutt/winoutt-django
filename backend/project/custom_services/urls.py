from django.urls import path
from . import views

urlpatterns = [
    path('pusher/auth', views.PusherAuth.as_view(), name="pusher_auth"),
]
