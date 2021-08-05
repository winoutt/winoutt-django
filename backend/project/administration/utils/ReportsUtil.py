# Model Imports
from project.reports.models import Report
from project.users.models import User
from project.posts.models import Post, Comment

# Library Imports
from django.contrib.contenttypes.models import ContentType

# Util Imports
from project.users.utils import UserUtil
from project.posts.utils import PostUtil, CommentUtil

def get_latest_reports():
    return Report.objects.all().order_by("-created_at")[0:50]


def approve_report(report):
    if report.reportable_type == ContentType.objects.get_for_model(User):
        UserUtil.ban_user(report.reportable_id)
    elif report.reportable_type == ContentType.objects.get_for_model(Post):
        post = PostUtil.get_post_or_exception(report.reportable_id)
        post.delete()
    elif report.reportable_type == ContentType.objects.get_for_model(Comment):
        comment = CommentUtil.get_comment_or_exception(report.reportable_id)
        comment.delete()
    else:
        raise Exception("Invalid take action request")
    

