from .models import Report
from project.posts.utils import PostUtil, CommentUtil
from project.users.utils import UserUtil

def get_reportable(reportable_id, report_type):
    if report_type == "comment":
        return CommentUtil.get_comment_or_exception(reportable_id)
    elif report_type == "post":
        return PostUtil.get_post_or_exception(reportable_id)
    elif report_type == "user":
        return UserUtil.get_user_from_id_or_raise_exception(reportable_id)

def get_report_or_exception(report_id):
    report = Report.objects.filter(report_id=report_id)
    if report.exists():
        return report.first()
    raise Exception("Unable to find report.")