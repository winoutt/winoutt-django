from project.posts.models import CommentVote

from project.posts.utils import CommentUtil

def create_comment_vote(user, comment_id):
    comment = CommentUtil.get_comment_or_exception(comment_id)
    if is_comment_vote_exist(user, comment):
        raise Exception("Already upvoted")
    comment_vote = CommentVote.objects.create(user=user, comment=comment)
    return comment_vote

def is_comment_vote_exist(user, comment):
    if CommentVote.objects.filter(user=user, comment=comment).exists():
        return True
    return False


def delete_comment_vote(user, comment_id):
    comment = CommentUtil.get_comment_or_exception(comment_id)
    if not is_comment_vote_exist(user, comment):
        raise Exception("Already unvoted")
    CommentVote.objects.get(user=user, comment=comment).delete()
    return comment

def get_comment_votes_count(comment):
    return CommentVote.objects.filter(comment=comment).count()