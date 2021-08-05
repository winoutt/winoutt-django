# Models Imports
from project.conversations.models import Chat, ChatArchive, Message
from project.posts.models import (
    Comment,
    CommentHashtag,
    CommentMention,
    AuthorStarView,
    CommentVote,
    Favorite,
    Hashtag,
    LinkPreview,
    PollChoice,
    PollVote,
    PostAlbum,
    PostHashtag,
    PostMention,
    PostUnfollow,
    Star,
    Team,
    Post,
)
from project.users.models import (
    Connection,
    Note,
    PeopleUnfollow,
    User,
    MALE,
    FEMALE,
    EndUser,
    Website,
)
from project.notifications.models import Notification
from project.reports.models import Report

from django.db.models import Count

# Library Imports
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta


def get_posts_analytics_counts():
    posts_analytics_counts = dict()
    posts_analytics_counts["count"] = Post.objects.count()
    posts_analytics_counts["texts"] = Post.objects.filter(
        postcontent__post_content_type="text"
    ).count()
    posts_analytics_counts["images"] = Post.objects.filter(
        postcontent__post_content_type="image"
    ).count()
    posts_analytics_counts["videos"] = Post.objects.filter(
        postcontent__post_content_type="video"
    ).count()
    posts_analytics_counts["audios"] = Post.objects.filter(
        postcontent__post_content_type="audio"
    ).count()
    posts_analytics_counts["documents"] = Post.objects.filter(
        postcontent__post_content_type="document"
    ).count()
    posts_analytics_counts["articles"] = Post.objects.filter(
        postcontent__post_content_type="article"
    ).count()
    posts_analytics_counts["albums"] = Post.objects.filter(
        postcontent__post_content_type="album"
    ).count()
    posts_analytics_counts["polls"] = Post.objects.filter(
        postcontent__post_content_type="poll"
    ).count()
    return posts_analytics_counts


def get_reportings_analytics_counts():
    reportings_analytics_counts = dict()
    reportings_analytics_counts["count"] = Report.objects.count()
    reportings_analytics_counts["users"] = Report.objects.filter(
        reportable_type=ContentType.objects.get_for_model(User)
    ).count()
    reportings_analytics_counts["posts"] = Report.objects.filter(
        reportable_type=ContentType.objects.get_for_model(Post)
    ).count()
    reportings_analytics_counts["comments"] = Report.objects.filter(
        reportable_type=ContentType.objects.get_for_model(Comment)
    ).count()
    return reportings_analytics_counts


def get_users_analytics_counts():
    users_analytics_counts = dict()
    users_analytics_counts["count"] = EndUser.objects.count()
    users_analytics_counts["males"] = EndUser.objects.filter(gender=MALE).count()
    users_analytics_counts["females"] = EndUser.objects.filter(gender=FEMALE).count()
    users_analytics_counts["online"] = EndUser.objects.filter(is_online=True).count()
    users_analytics_counts["banned"] = EndUser.objects.filter(status="banned").count()
    return users_analytics_counts


def get_websites_analytics_counts():
    websites_analytics_counts = dict()
    websites_analytics_counts["count"] = (
        Website.objects.filter(personal__isnull=False).count()
        + Website.objects.filter(company__isnull=False).count()
    )
    websites_analytics_counts["personal"] = Website.objects.filter(
        personal__isnull=False
    ).count()
    websites_analytics_counts["company"] = Website.objects.filter(
        company__isnull=False
    ).count()
    return websites_analytics_counts


def get_count():
    counts = dict()
    counts["chats"] = Chat.objects.count()
    counts["chatArchives"] = ChatArchive.objects.count()
    counts["comments"] = Comment.objects.count()
    counts["commentHashtags"] = CommentHashtag.objects.count()
    counts["commentMentions"] = CommentMention.objects.count()
    counts["authorStarViews"] = AuthorStarView.objects.count()
    counts["commentVotes"] = CommentVote.objects.count()
    counts["connections"] = Connection.objects.count()
    counts["favorites"] = Favorite.objects.count()
    counts["hashtags"] = Hashtag.objects.count()
    counts["lastMessages"] = Chat.objects.count()
    counts["linkPreviews"] = LinkPreview.objects.count()
    counts["messages"] = Message.objects.count()
    counts["notes"] = Note.objects.count()
    counts["notifications"] = Notification.objects.count()
    counts["pollChoices"] = PollChoice.objects.count()
    counts["pollVotes"] = PollVote.objects.count()
    counts["postAlbumPhotos"] = PostAlbum.objects.count()
    counts["postHashtags"] = PostHashtag.objects.count()
    counts["postMentions"] = PostMention.objects.count()
    counts["posts"] = get_posts_analytics_counts()
    counts["postUnfollows"] = PostUnfollow.objects.count()
    counts["reportings"] = get_reportings_analytics_counts()
    counts["stars"] = Star.objects.count()
    counts["teams"] = Team.objects.count()
    counts["unfollows"] = PeopleUnfollow.objects.count()
    counts["users"] = get_users_analytics_counts()
    counts["websites"] = get_websites_analytics_counts()
    return counts


def get_top_countries():
    countries = (
        EndUser.objects.filter(country__isnull=False)
        .values("country")
        .annotate(count=Count("country"))
        .values_list("country", flat=True)
        .order_by("-count")[0:10]
    )
    return countries


def get_users_monthly_statistics():
    today = datetime.now()
    one_month_ago = datetime.now() - timedelta(30)
    users_count = EndUser.objects.filter(
        created_at__range=[one_month_ago, today]
    ).count()
    return users_count


def get_posts_monthly_statistics():
    today = datetime.now()
    one_month_ago = datetime.now() - timedelta(30)
    posts_count = Post.objects.filter(created_at__range=[one_month_ago, today]).count()
    return posts_count


def get_stars_monthly_statistics():
    today = datetime.now()
    one_month_ago = datetime.now() - timedelta(30)
    stars_count = Star.objects.filter(created_at__range=[one_month_ago, today]).count()
    return stars_count


def get_comments_monthly_statistics():
    today = datetime.now()
    one_month_ago = datetime.now() - timedelta(30)
    comments_count = Comment.objects.filter(
        created_at__range=[one_month_ago, today]
    ).count()
    return comments_count


def get_monthly_statistics():
    statistics = dict()
    statistics["users"] = get_users_monthly_statistics()
    statistics["posts"] = get_posts_monthly_statistics()
    statistics["stars"] = get_stars_monthly_statistics()
    statistics["comments"] = get_comments_monthly_statistics()
    return statistics
