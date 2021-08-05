from project.posts.models import Favorite
from project.posts.utils import PostUtil


def create(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if is_favorite_post_exist(user, post):
        raise Exception("Already favorited")
    favorite = Favorite.objects.create(user=user, post=post)
    return favorite


def is_favorite_post_exist(user, post):
    if Favorite.objects.filter(user=user, post=post).exists():
        return True
    return False


def delete(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if not is_favorite_post_exist(user, post):
        raise Exception("Already deleted")
    Favorite.objects.get(user=user, post=post).delete()


def paginate(user):
    favorite_post_ids = (
        Favorite.objects.filter(user=user)
        .order_by("-favorite_id")
        .values_list("post", flat=True)
    )
    return PostUtil.get_posts_from_ids(favorite_post_ids)
