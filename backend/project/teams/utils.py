# Model imports
from .models import Team as TeamModel
from project.posts.models import Post
from project.users.models import User

# Library Imports
from django.db.models import Count, Q


def get_top_teams():
    teams = TeamModel.objects.annotate(post_count=Count("post")).order_by(
        "-post_count"
    )[:3]
    return teams


def get_team_from_slug_or_exception(slug):
    team = TeamModel.objects.filter(slug=slug)
    if team.exists():
        return team.first()
    raise Exception("Team not found.")


def get_team_from_id_or_exception(team_id):
    team = TeamModel.objects.filter(team_id=team_id)
    if team.exists():
        return team.first()
    raise Exception("Team not found.")


def get_contributers(team_id):
    team = get_team_from_id_or_exception(team_id)
    users_ids = Post.objects.filter(team=team).values_list("user", flat=True).distinct()
    users = User.objects.filter(id__in=users_ids).annotate(
        post_count=Count("post", filter=Q(post__team=team), distinct=True),
         comment_count=Count("comment", filter=Q(comment__post__team=team), distinct=True)
         ).order_by("-post_count", "-comment_count")[0:5]
    return users

def get_team_posts(team_id):
    team = get_team_from_id_or_exception(team_id)
    posts = Post.objects.filter(team=team).order_by('-post_id')
    return posts

