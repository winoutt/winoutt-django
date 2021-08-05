from . import views
from django.urls import path

urlpatterns = [
    path('api/contact', views.Contact.as_view(), name='contact'),
]
