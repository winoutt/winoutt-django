from project.posts.models import PostUnfollow
from project.posts.utils import PostUtil


def is_post_unfollowed(user, post):
    return PostUnfollow.objects.filter(user=user, post=post).exists()


def create(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if is_post_unfollowed(user, post):
        raise Exception("Already unfollowed")
    PostUnfollow.objects.create(user=user, post=post)
    return post


def delete(user, post_id):
    post = PostUtil.get_post_or_exception(post_id)
    if not is_post_unfollowed(user, post):
        raise Exception("Already followed")
    PostUnfollow.objects.get(user=user, post=post).delete()
    return post