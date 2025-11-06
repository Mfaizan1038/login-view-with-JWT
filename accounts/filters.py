import django_filters
from accounts.models import User

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']
        