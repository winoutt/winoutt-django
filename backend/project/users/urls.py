from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Profile Urls
    path("api/auth/register", views.UserRegister.as_view(), name="register"),
    path("api/auth/login", views.UserLogin.as_view(), name="login"),
    path("api/auth/logout", views.UserLogout.as_view(), name="logout"),
    path(
        "api/verification/resend",
        views.ResendVerificationEmail.as_view(),
        name="resend_verification_mail",
    ),
    # Password Reset Urls
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView,
        name="password_reset_done",
    ),
    re_path(
        "reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        auth_views.PasswordResetConfirmView,
        name="password_reset_confirm",
    ),
    path(
        "reset/done/", auth_views.PasswordResetDoneView, name="password_reset_complete"
    ),
    # Connection Urls
    path("api/connections", views.Connection.as_view(), name="connections"),
    re_path(
        "api/connections/(?P<id>\d+)/accept",
        views.AcceptConnection.as_view(),
        name="accept_connection",
    ),
    re_path(
        "api/connections/(?P<id>\d+)/ignore",
        views.IgnoreConnection.as_view(),
        name="ignore_connection",
    ),
    re_path(
        "api/connections/(?P<id>\d+)/mutuals",
        views.MutualConnection.as_view(),
        name="mutuals_connection",
    ),
    re_path(
        "api/connections/(?P<id>\d+)/disconnect",
        views.Disconnect.as_view(),
        name="disconnect_connection",
    ),
    re_path(
        "api/connections/(?P<id>\d+)/cancel",
        views.CancelConnection.as_view(),
        name="cancel_connection",
    ),
    re_path(
        "api/connections/(?P<id>\d+)",
        views.ListConnection.as_view(),
        name="list_connection",
    ),
    # Notes Urls
    path("api/notes", views.Note.as_view(), name="notes"),
    path("api/notes/<int:pk>", views.EditNote.as_view(), name="edit_note"),
    path("api/notes/archived", views.ArchivedNoteList.as_view(), name="archived_notes"),
    path("api/notes/<int:pk>/archive", views.ArchiveNote.as_view(), name="archive_note"),
    path("api/notes/blanks", views.DeleteBlankNotes.as_view(), name="delete_blank_notes"),
    re_path(
        "api/notes/(?P<id>\d+)/unarchive",
        views.UnArchivedNote.as_view(),
        name="unarchive_notes",
    ),
    
    # People urls
    path('api/people/mayknow', views.PeopleMayKnow.as_view(), name='mayknow'),
    path('api/people/paginate', views.PeopleMayKnowPaginator.as_view(), name='mayknow_paginator'),
    path('api/people/search', views.PeopleSearch.as_view(), name='search'),

    # User Urls
    path('api/users', views.EditUser.as_view(), name='edit_user'),
    path('api/users/status', views.UpdateUserStatus.as_view(), name='update_status'),
    path('api/users/<str:username>', views.ReadUser.as_view(), name='read_user'),
    path('api/users/<str:username>/posts', views.ReadUserPosts.as_view(), name='read_user_posts'),


    # People Unfollow Urls
    path('api/unfollows', views.PeopleUnfollow.as_view(), name='people_unfollow_create'),
    path('api/unfollows/<int:user_connection_id>', views.PeopleUnfollow.as_view(), name='people_unfollow_delete'),

    # Auth Urls
    path('api/auth/user', views.AuthUser.as_view(), name='get_auth_user'),
    path('api/sessions', views.UpdateSession.as_view(), name='update_session'),
    path('api/settings', views.UpdateSetting.as_view(), name='update_setting'),
    path('api/passwords', views.ChangePassword.as_view(), name='change_password'),

    # Search Urls
    path('api/search/all', views.SearchAll.as_view(), name='search_all'),


]
