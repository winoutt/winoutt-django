from project.posts.models import PollVote

def is_poll_vote_exist(poll, user):
    return PollVote.objects.filter(user=user, poll=poll)


def get_post_poll_votes_count(post):
    return PollVote.objects.filter(poll__post=post).count()

def get_poll_choice_vote_count(poll_choice):
    return PollVote.objects.filter(poll_choice=poll_choice).count()


def is_poll_choice_vote_exist(user, poll_choice):
    return PollVote.objects.filter(user=user, poll_choice=poll_choice)