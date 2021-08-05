from project.posts.models import PostContent

def check_text_types(data):
    errors = []
    if data.get('caption', None) is None:
        errors.append("caption is required.")
    return errors

def check_article_types(data):
    errors = []
    if data.get('caption', None) is None:
        errors.append("caption is required.")
    return errors


def get_post_content_or_None(post):
    post_content = PostContent.objects.filter(post=post)
    if post_content.exists():
        return post_content.first()
    return None