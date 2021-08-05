from project.posts.models import Post
from django.db.models import Q

def get_posts_list():
    return Post.objects.all().order_by("-created_at")[0:25]

def search_posts(term):
    if not term:
        return None
    posts = Post.objects.filter(Q(postcontent__post_content_type__icontains=term) | Q(user__email__icontains=term)).order_by("-post_id")[0:25]
    return posts