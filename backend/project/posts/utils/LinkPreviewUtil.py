from project.posts.models import LinkPreview, Post
from project.conversations.models import Message
from django.contrib.contenttypes.models import ContentType


def create(post, data):
    image = data.get('image:secure_url', None)
    if image is None:
        image = data['image']
    LinkPreview.objects.create(title=data['title'],
                             description=data['description'],
                            url=data['url'],
                            image=data['image'],
                            previewable=post)


def get_post_link_preview(post):
    return LinkPreview.objects.filter(previewable_type=ContentType.objects.get_for_model(Post), previewable_id=post.post_id)


def get_message_link_preview(message):
    return LinkPreview.objects.filter(previewable_type=ContentType.objects.get_for_model(Message), previewable_id=message.message_id)