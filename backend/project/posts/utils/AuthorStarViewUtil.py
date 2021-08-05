from project.posts.models import AuthorStarView

def create(user, post):
    return AuthorStarView.objects.create(user=user, post=post)

def is_author_star_view_exist(user, post):
    return AuthorStarView.objects.filter(user=user, post=post).exists()

def mark_author_viewed(user, post):
    is_viewed = is_author_star_view_exist(user, post)
    if not is_viewed:
        create(user, post)
    return is_viewed