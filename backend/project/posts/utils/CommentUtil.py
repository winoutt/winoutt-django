from project.posts.models import Comment
from project.posts.utils import PostUtil

def get_comment_or_exception(comment_id, user=None):
    if user is not None:
        comment = Comment.objects.filter(user=user, comment_id=comment_id)
        if comment.exists():
            return comment.first()
    else:
        comment = Comment.objects.filter(comment_id=comment_id)
        if comment.exists():
            return comment.first()
    raise Exception("Unable to delete the comment.")

# def get_comment_or_exception(comment_id):
#     comment = Comment.objects.filter(comment_id=comment_id)
#     print(comment)
#     if comment.exists():
#         return comment.first()
#     raise Exception("Comment not found.")


def paginate(post_id):
    post = PostUtil.get_post_or_exception(post_id)
    comments = Comment.objects.filter(post=post).order_by("-comment_id")
    return comments

def get_post_comments_count(post):
    return Comment.objects.filter(post=post).count()