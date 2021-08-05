from project.posts.models import PollChoice

def get_poll_choices_or_None(poll):
    choices = PollChoice.objects.filter(poll=poll)
    if choices.exists():
        return choices
    return None

def create(poll, choices):
    for choice in choices:
        PollChoice.objects.create(value=choice, poll=poll)