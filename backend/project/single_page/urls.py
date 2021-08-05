from django.urls import path, re_path
from . import views

# added for django-vue integration purpose
from django.views.generic import TemplateView

urlpatterns = [
    re_path('^$', TemplateView.as_view(template_name="index.html"), name="app",),
    re_path('^(?:.*)/?$', TemplateView.as_view(template_name="index.html")),
]
