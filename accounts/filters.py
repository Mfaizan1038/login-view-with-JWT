import django_filters
from accounts.models import User
from django.db.models import F, Value
from django.db.models.functions import Substr, StrIndex, Length


class UserFilter(django_filters.FilterSet):
    email_domain = django_filters.CharFilter(method='filter_by_email_domain')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'email_domain']

    def filter_by_email_domain(self, queryset, name, value):
        
        queryset = queryset.annotate(at_pos=StrIndex(F('email'), Value('@')) ).annotate(domain=Substr(F('email'), F('at_pos') + 1, Length(F('email'))) )
        return queryset.filter(domain=value)
        

