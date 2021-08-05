from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as mail_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include(("project.users.urls", "users"), namespace="users",),),
    path(
        "help/",
        include(("project.help.urls", "help"), namespace="help"),
    ),
    path("teams/", include(("project.teams.urls", "teams"), namespace="teams")),
    path("posts/", include(("project.posts.urls", "posts"), namespace="posts")),
    path(
        "conversations/",
        include(
            ("project.conversations.urls", "conversations"), namespace="conversations"
        ),
    ),
    path(
        "notifications/",
        include(
            ("project.notifications.urls", "notifications"), namespace="notifications"
        ),
    ),
    path("reports/", include(("project.reports.urls", "reports"), namespace="reports")),
    path(
        "custom_services/",
        include(
            ("project.custom_services.urls", "custom_services"),
            namespace="custom_services",
        ),
    ),
    path(
        "administration/",
        include(
            ("project.administration.urls", "administration"),
            namespace="administration",
        ),
    ),
    path("email/", include(mail_urls)),
    path(
        "",
        include(("project.single_page.urls", "single_page"), namespace="single_page"),
    ),
]
