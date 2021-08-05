# Library Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Model Imports
from .models import Comment, Post

# Serializer Imports
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    CreatePostSerializer,
    PostSerializer,
    HashtagSerializer,
    PostCountSerializer,
    FavoriteSerializer,
    StarSerializer,
    PostDetailSerializer,
)
from project.users.serializers import UserSerializer

# Utils Imports
from .utils import (
    CommentUtil,
    PostUtil,
    CommentMentionUtil,
    CommentHashTagUtil,
    CommentVoteUtil,
    StarUtil,
    FavoriteUtil,
    PostMentionUtil,
    PostUnfollowUtil,
    HashtagUtil,
    PollChoiceUtil,
    PostAlbumUtil,
    PostHashtagUtil,
)
from project.notifications import utils as NotificationUtil
from project.custom_services import MetaDataService, PusherEvents, ACM
from project.posts.utils import LinkPreviewUtil


# Form Imports
from .forms import PollVoteForm, PostForm, PostContentForm, PollForm

# Comment Views


class Comment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        comment_serializer = CommentSerializer(data=data)
        if not comment_serializer.is_valid():
            return Response(
                comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            comment = comment_serializer.save()

            comment_mentions = CommentMentionUtil.create(comment)
            CommentHashTagUtil.create(comment)

            NotificationUtil.send_notification_to_comment_mentions(
                request.user, comment_mentions
            )
            NotificationUtil.send_comment_notification_to_user(request.user, comment)
            NotificationUtil.send_notification_to_all_commentees(request.user, comment)
            NotificationUtil.send_comment_notification_to_post_stared_users(
                request.user, comment
            )
        except Exception as error:
            errors = {"error": ["Unable to create comment"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            CommentDetailSerializer(comment, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class DeleteComment(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            comment = CommentUtil.get_comment_or_exception(pk, request.user)
        except Exception as error:
            errors = {"error": ["Unable to delete the comment."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        comment.delete()
        return Response({"isDeleted": True}, status=status.HTTP_200_OK)


class CommentsPaginator(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None, *args, **kwargs):
        try:
            comments = CommentUtil.paginate(pk)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(comments, request)
            comment_serializer = CommentDetailSerializer(
                results, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(comment_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Comment Vote Views


class CommentVote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        try:
            comment_id = kwargs.get("comment_id", None)
            comment_vote = CommentVoteUtil.create_comment_vote(request.user, comment_id)
            NotificationUtil.send_notification_to_comment_owner_on_upvote(
                request.user, comment_vote.comment
            )
            return Response(
                CommentDetailSerializer(
                    comment_vote.comment, context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, format=None):
        try:
            comment = CommentVoteUtil.delete_comment_vote(request.user, comment_id)
            return Response(
                CommentDetailSerializer(comment, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Comment Mention Views


class CommentMentionSuggestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            post_id = self.request.query_params.get("post")
            users = CommentMentionUtil.get_mention_suggestions(request.user, post_id)
            return Response(
                UserSerializer(users, many=True, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SearchCommentMentionSuggestions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            post_id = self.request.query_params.get("post")
            term = self.request.query_params.get("term")
            if term is None:
                raise Exception("Term is not provided.")
            users = CommentMentionUtil.search_mention_suggestions(
                request.user, post_id, term
            )
            return Response(
                UserSerializer(users, many=True, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Start Post Views


class StarPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        try:
            post_id = request.data.get("postId")
            if post_id is None:
                raise Exception("postId is not provided.")
            star = StarUtil.create(request.user, post_id)
            NotificationUtil.send_star_notification_to_user(request.user, star)
            return Response({"isStared": True}, status=status.HTTP_201_CREATED)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        try:
            StarUtil.delete(request.user, post_id)
            return Response({"isUnstared": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Post Favorite Urls


class PostFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            posts = FavoriteUtil.paginate(request.user)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(posts, request)
            posts_serializer = PostDetailSerializer(
                results, many=True, context={"request": request}
            )
            return paginator.get_paginated_response(posts_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None, *args, **kwargs):
        try:
            post_id = request.data.get("postId")
            if post_id is None:
                raise Exception("postId is not provided.")
            favorite = FavoriteUtil.create(request.user, post_id)
            return Response({"isFavorited": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        try:
            FavoriteUtil.delete(request.user, post_id)
            return Response({"isDeleted": True}, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Post Views
class Post(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, *args, **kwargs):
        # try:
        # Post Form
        post_form = PostForm(request.data)
        if not post_form.is_valid():
            return Response(
                {"message": post_form.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        post = post_form.save(commit=False)
        post.user = request.user

        # Post Content Form
        post_content_form = PostContentForm(request.data)
        if not post_content_form.is_valid():
            return Response(
                {"message": post_content_form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post_content = post_content_form.save(commit=False)

        if post_content.post_content_type == "poll":
            choices = request.data.get("choices")
            # Poll Form
            poll_form = PollForm(request.data, choices=choices)
            if not poll_form.is_valid():
                return Response(
                    {"message": poll_form.errors}, status=status.HTTP_400_BAD_REQUEST
                )
            poll = poll_form.save(commit=False)
        else:
            poll = None
        if post_content.post_content_type == "album":
            photos = request.data.get("photos")
            if photos is None:
                raise Exception("photos are required.")

        # Save Data to Database
        post.save()
        post_content.post = post
        post_content.save()
        if post_content.post_content_type == "poll":
            poll.post = post
            poll.save()
            PollChoiceUtil.create(poll, choices)
        if post_content.post_content_type == "album":
            PostAlbumUtil.create(post, photos)
        url = MetaDataService.get_url(post.caption)
        if url is not None:
            data = MetaDataService.get_metadata(url)
            LinkPreviewUtil.create(post, data)
        PusherEvents.broad_cast_post_created_message(post, {"post_id": post.post_id})
        NotificationUtil.send_create_post_notification(post)
        post_mentions = PostMentionUtil.create(post)
        for post_mention in post_mentions:
            NotificationUtil.send_post_mention_notification(post.user, post_mention)
        PostHashtagUtil.create(post)
        payload = {"type": "post", "id": post.post_id}
        # ACM.get_acm_reponse(payload)
        # except Exception as error:
        #     errors = {"error": [str(error)]}
        #     return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            PostDetailSerializer(post, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, post_id, format=None, *args, **kwargs):
        try:
            post = PostUtil.get_post_or_exception_on_user(post_id, request.user)
        except Exception as error:
            errors = {"error": ["Unable to delete the post."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response({"isDeleted": True}, status=status.HTTP_200_OK)

    def get(self, request, post_id, format=None, *args, **kwargs):
        try:
            post = PostUtil.get_post_or_exception(post_id)
        except Exception as error:
            errors = {"error": ["Sorry, this post has been removed."]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            PostDetailSerializer(post, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )


class StarPostPaginator(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, format=None, *args, **kwargs):
        try:
            data = StarUtil.paginate(request.user, post_id)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(data["stars"], request)
            users = StarUtil.get_stared_post_users(post_id)            
            user_serializer = UserSerializer(users, many=True, context={'request':request})
            return Response(
                {
                    "is_author_star_viewed": data["is_author_star_viewed"],
                    "stars":{
                    "results": user_serializer.data,
                    "next": paginator.get_next_link(),
                    "count": paginator.page.paginator.count,
                    "previous": paginator.get_previous_link()
                    }
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class PostMentionSuggestion(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            suggestions = PostMentionUtil.get_suggestions(request.user)
            return Response(
                UserSerializer(
                    suggestions, many=True, context={"request": request}
                ).data,
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            errors = {"error": ["Unable to suggest users"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SearchPostMentionSuggestion(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            term = self.request.query_params.get("term")
            suggestions = PostMentionUtil.get_search_suggestions(request.user, term)
            return Response(
                UserSerializer(
                    suggestions, many=True, context={"request": request}
                ).data,
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            errors = {"error": ["Unable to suggest users"]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class PostUnfollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, format=None, *args, **kwargs):
        try:
            post = PostUnfollowUtil.create(request.user, post_id)
            return Response(
                PostDetailSerializer(post, context={"request": request}).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None, *args, **kwargs):
        try:
            post = PostUnfollowUtil.delete(request.user, post_id)
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TopPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            posts = PostUtil.get_top_posts()
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            PostDetailSerializer(posts, many=True, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


# Poll Vote Views
class PollVote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            poll_vote_form = PollVoteForm(request.data, request=request)
            if not poll_vote_form.is_valid():
                return Response(
                    poll_vote_form.errors, status=status.HTTP_400_BAD_REQUEST
                )
            poll_vote = poll_vote_form.save()
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            PostDetailSerializer(
                poll_vote.poll.post, context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED,
        )


# Hashtags Views


class TrendingHashtags(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        try:
            hashtags = HashtagUtil.get_trending_hashtags()
            return Response(
                HashtagSerializer(hashtags, many=True).data, status=status.HTTP_200_OK
            )
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class HashtagPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, hashtag, format=None, *args, **kwargs):
        try:
            posts = HashtagUtil.get_posts(hashtag)
            paginator = PageNumberPagination()
            results = paginator.paginate_queryset(posts, request)
            post_serializer = PostDetailSerializer(
                results, context={"request": request}, many=True
            )
            return paginator.get_paginated_response(post_serializer.data)
        except Exception as error:
            errors = {"error": [str(error)]}
            return Response(errors, status=status.HTTP_404_NOT_FOUND)
