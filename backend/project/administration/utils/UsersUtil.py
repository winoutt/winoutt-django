from project.users.models import User, EndUser
from django.db.models import Q

def get_users_list():
    end_users = EndUser.objects.all().values_list("user", flat=True).order_by("-created_at")[0:25]
    return User.objects.filter(id__in=end_users)


def search_users(term):
    if not term:
        return None
    end_users = EndUser.objects.filter(
                Q(user__first_name__icontains=term) |
                Q(user__last_name__icontains=term) |
                Q(user__username__icontains=term) | 
                Q(user__email__icontains=term) |
                Q(city__icontains=term) |
                Q(gender__icontains=term) |
                Q(country__icontains=term)).values_list("user", flat=True).order_by("-end_user_id")[0:25]
    return User.objects.filter(id__in=end_users)


def get_emails():
    return User.objects.filter(email__isnull=False).exclude(email__exact='').values_list("email", flat=True)