# Model Imports
from .models import PollVote, Poll, PollChoice, Post, post_content_types, PostContent

# Util Imports
from .utils import PollVoteUtil
import base64
from django.core.files.base import ContentFile


# Library Imports
from datetime import datetime, timedelta
from django.utils import timezone
from django.forms import (
    Form,
    ModelForm,
    BooleanField,
    CharField,
    ValidationError,
    MultipleChoiceField,
)


class PollVoteForm(ModelForm):
    class Meta:
        model = PollVote
        fields = ("poll", "poll_choice")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PollVoteForm, self).__init__(*args, **kwargs)
        self.fields["poll"].error_messages["required"] = "poll is required."
        self.fields["poll_choice"].error_messages[
            "required"
        ] = "poll_choice is required."

    def clean(self):
        poll = self.cleaned_data.get("poll", None)
        poll_choice = self.cleaned_data.get("poll_choice", None)

        if poll_choice is not None and poll_choice.poll != poll:
            raise ValidationError("Invalid poll choice.")
        if poll is not None and poll.post.user == self.request.user:
            raise ValidationError("You can't vote to poll.")
        if PollVoteUtil.is_poll_vote_exist(poll, self.request.user):
            raise ValidationError("Already voted to poll.")

    def save(self, commit=True):
        poll = self.cleaned_data.get("poll", None)
        poll_choice = self.cleaned_data.get("poll_choice", None)
        poll_vote = PollVote.objects.create(
            user=self.request.user, poll=poll, poll_choice=poll_choice
        )
        return poll_vote


class PostForm(ModelForm):

    post_content_type = CharField(required=True)

    class Meta:
        model = Post
        fields = ("team", "caption", "post_content_type")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["team"].error_messages["required"] = "team is required."
        self.fields["team"].error_messages["invalid_choice"] = "Provide valid team."
        self.fields["post_content_type"].error_messages[
            "required"
        ] = "post_content_type is required."

    def clean(self):
        post_content_type = self.cleaned_data.get("post_content_type", None)
        caption = self.cleaned_data.get("caption", None)
        if (
            post_content_type is not None
            and post_content_type not in post_content_types
        ):
            raise ValidationError("Invalid post_content_type.")
        if (
            post_content_type is not None
            and post_content_type == "text"
            and (caption is None or caption == "")
        ):
            raise ValidationError("caption is required.")

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=commit)
        return post


class PostContentForm(ModelForm):
    cover = CharField(required=False)

    class Meta:
        model = PostContent
        fields = ("body", "cover", "post_content_type", "photo_original")

    def clean(self):
        cover = self.cleaned_data.get("cover", None)
        filename = self.cleaned_data.get("filename", None)
        post_content_type = self.cleaned_data.get("post_content_type", None)

    def save(self, commit=True):
        post_content = super(PostContentForm, self).save(commit=commit)
        cover = self.cleaned_data.get("cover", None)
        if cover is not None and cover != "":
            format, imgstr = cover.split(";base64,")
            ext = format.split("/")[-1]
            cover = ContentFile(base64.b64decode(imgstr), name="post_cover." + ext)
            post_content.cover = cover
            post_content.cover_original = cover

        return post_content


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ("question", "end_at")

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super(PollForm, self).__init__(*args, **kwargs)
        self.fields["question"].error_messages["required"] = "question is required."
        self.fields["end_at"].error_messages["required"] = "end_at is required."

    def clean(self):
        end_at = self.cleaned_data.get("end_at", None)
        if end_at is not None and end_at < (timezone.now() - timedelta(minutes=1)):
            raise ValidationError("end_at must be a future date time.")
        if self.choices is None:
            raise ValidationError("Choices are required.")

    def save(self, commit=True):
        poll = super(PollForm, self).save(commit=commit)
        return poll
