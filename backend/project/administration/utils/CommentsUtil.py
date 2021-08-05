from project.posts.models import Comment
from django.db.models import Q

def get_comments_list():
    return Comment.objects.all().order_by("-created_at")[0:25]

def search_comments(term):
    if not term:
        return None
    comments = Comment.objects.filter(Q(comment_id__icontains=term) | Q(user__email__icontains=term)).order_by("-comment_id")[0:25]
    return comments