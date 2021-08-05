from project.posts.models import Poll

def get_poll_or_None(post):
    poll = Poll.objects.filter(post=post)
    if poll.exists():
        return poll.first()
    return None