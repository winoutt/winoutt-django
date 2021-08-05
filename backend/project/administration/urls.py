from . import views
from django.urls import path

urlpatterns = [
    # Analytics Urls
    path('api/analytics/counts', views.AnalyticsCount.as_view(), name='get_analytics_count'),
    path('api/analytics/countries/top', views.TopCountries.as_view(), name='get_top_countries'),
    path('api/analytics/statistics/monthly', views.MonthlyStatistics.as_view(), name='get_monthly_statistics'),

    # Reporting Urls
    path('api/reportings', views.ReportsList.as_view(), name='get_reports_list'),
    path('api/reportings/<int:report_id>', views.Report.as_view(), name='get_report_from_id'),
    path('api/reportings/<int:report_id>/approve', views.Report.as_view(), name='approve_report_request'),

    # User Urls
    path('api/users', views.UsersList.as_view(), name='get_users_list'),
    path('api/users/search', views.SearchUsers.as_view(), name='search_users'),
    path('api/users/<int:user_id>', views.ReadUser.as_view(), name='read_user'),
    path('api/users/<int:user_id>/block', views.BlockUser.as_view(), name='block_user'),
    path('api/users/<int:user_id>/unblock', views.UnblockUser.as_view(), name='unblock_user'),

    # Posts Urls
    path('api/posts', views.PostsList.as_view(), name='get_posts_list'),
    path('api/posts/search', views.SearchPosts.as_view(), name='search_posts'),
    path('api/posts/<int:post_id>', views.Post.as_view(), name='post'),

    # Comments Urls
    path('api/comments', views.CommentsList.as_view(), name='get_comments_list'),
    path('api/comments/search', views.SearchComments.as_view(), name='search_comments'),
    path('api/comments/<int:comment_id>', views.Comment.as_view(), name='comment'),
    
    # Admin Urls
    path('api/admins/password', views.UpdateAdminPassword.as_view(), name='update_admin_password'),
    path('api/mails/send', views.SendEmail.as_view(), name='send_email_from_admin'),
    path('api/auth/check', views.AuthCheck.as_view(), name='auth_check'),
    path('api/socket/auth', views.AuthSocket.as_view(), name='auth_socket'),

    # Admin Login Urls
    path("api/admin/login", views.AdminLogin.as_view(), name="admin_login"),
   


]
