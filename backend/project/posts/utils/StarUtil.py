from project.posts.models import Star, Post
from project.posts.utils import PostUtil, AuthorStarViewUtil
from project.users.utils import UserUtil

def create(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if user.id == post.user.id:
        raise Exception("You can't star your own post")
    if is_start_post_exist(user, post):
        raise Exception("Already stared")
    star = Star.objects.create(user=user, post=post)
    return star

def is_start_post_exist(user, post):
    if Star.objects.filter(user=user, post=post).exists():
        return True
    return False

def delete(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if not is_start_post_exist(user, post):
        raise Exception("Already unstared")
    star = Star.objects.get(user=user, post=post).delete()


def paginate(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if post.user != user:
        raise Exception("You don't have permission to view the stars")
    is_author_star_viewed = AuthorStarViewUtil.mark_author_viewed(user, post)
    stars = Star.objects.filter(post=post).order_by("-star_id")
    data = {"is_author_star_viewed": is_author_star_viewed, "stars": stars}
    return data

def get_post_stars_count(post):
    return Star.objects.filter(post=post).count()


def get_star_or_None(star_id):
    star = Star.objects.filter(star_id=star_id)
    if star.exists():
        return star.first()
    return None


def get_stared_post_users(post):
    user_ids = Star.objects.filter(post=post).values_list("user", flat=True)
    return UserUtil.get_users(user_ids)