from django.urls import path, re_path
from . import views

urlpatterns = [
    # Comment Urls
    path("api/comments", views.Comment.as_view(), name="comments"),
    path("api/comments/<int:pk>", views.DeleteComment.as_view(), name="delete_comment"),
    path(
        "api/comments/<int:pk>/paginate",
        views.CommentsPaginator.as_view(),
        name="paginate_comments",
    ),
    # Comment Vote Url
    path(
        "api/comments/<int:comment_id>/votes",
        views.CommentVote.as_view(),
        name="comment_vote",
    ),
    # Comment Mention Url
    path(
        "api/comments/mentions/suggestions",
        views.CommentMentionSuggestions.as_view(),
        name="mention_suggestions",
    ),
    path(
        "api/comments/mentions/suggestions/search",
        views.SearchCommentMentionSuggestions.as_view(),
        name="search_mention_suggestions",
    ),
    # Post Star Urls
    path("api/stars", views.StarPost.as_view(), name="star_post"),
    path("api/stars/<int:post_id>", views.StarPost.as_view(), name="delete_star"),
    # Post Favorite Urls
    path("api/favorites", views.PostFavorite.as_view(), name="post_favorite"),
    path(
        "api/favorites/<int:post_id>",
        views.PostFavorite.as_view(),
        name="post_favorite",
    ),
    path(
        "api/favorites/paginate",
        views.PostFavorite.as_view(),
        name="post_favorite_paginator",
    ),
    # Post Urls
    path("api/posts", views.Post.as_view(), name="posts"),
    path("api/posts/<int:post_id>", views.Post.as_view(), name="delete_post"),
    path(
        "api/posts/<int:post_id>/stars",
        views.StarPostPaginator.as_view(),
        name="get_stared_post",
    ),
    path(
        "api/posts/mentions/suggestions",
        views.PostMentionSuggestion.as_view(),
        name="post_mention_suggestions",
    ),
    path(
        "api/posts/mentions/suggestions/search",
        views.SearchPostMentionSuggestion.as_view(),
        name="search_post_mention_suggestions",
    ),
    path(
        "api/posts/<int:post_id>/unfollows",
        views.PostUnfollow.as_view(),
        name="create_post_unfollow",
    ),
    path("api/posts/top", views.TopPosts.as_view(), name="get_top_posts"),
    # Poll Vote Urls
    path("api/poll/votes", views.PollVote.as_view(), name="create_poll_vote"),
    # Hash Tag Urls
    path(
        "api/hashtags/trending",
        views.TrendingHashtags.as_view(),
        name="get_trending_hashtags",
    ),
    path(
        "api/hashtags/<str:hashtag>/posts",
        views.HashtagPosts.as_view(),
        name="get_posts_of_hashtag",
    ),
]
