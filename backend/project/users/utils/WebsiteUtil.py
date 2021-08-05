from project.users.models import Website, User


def get_all_users_similar_company(company):
    user_ids = Website.objects.filter(company=company).values_list("user", flat=True)
    return User.objects.filter(id__in=user_ids)
