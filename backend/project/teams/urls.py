from . import views
from django.urls import path

urlpatterns = [
    path("api/teams", views.Team.as_view(), name="teams"),
    path("api/teams/top", views.TopTeam.as_view(), name="top_teams"),
    path("api/teams/<slug:slug>", views.ReadTeam.as_view(), name="read_team"),
    path("api/teams/<int:team_id>/contributors", views.TeamContributers.as_view(), name="get_team_contributers"),
    path("api/teams/<int:team_id>/posts", views.TeamPosts.as_view(), name="get_team_posts"),
]
