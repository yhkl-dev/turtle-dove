import django_filters
from django.db.models import Q
from .models import Resource, ResourceUser


class ResourcesFilter(django_filters.rest_framework.FilterSet):
    """
    资源过滤类
    """
    resource_name = django_filters.CharFilter(method='search_resource')
    manage_ip = django_filters.CharFilter(method="search_manage_ip")
    service = django_filters.NumberFilter(method="search_first_product")
    server_purpose = django_filters.NumberFilter(method="search_second_product")
    resource_type = django_filters.NumberFilter(method='search_resource_type')

    def search_server_type(self, queryset, name, value):
        if value == 0:
            return queryset.filter(server_type__in=[0, 1])
        else:
            return queryset.filter(server_type=value)

    def search_resource_type(self, queryset, name, value):
        return queryset.filter(resource_type__exact=value)

    def search_second_product(self, queryset, name, value):
        if value > 0:
            return queryset.filter(server_purpose_id__exact=value)
        elif value == -1:
            return queryset.filter(server_purpose_id__isnull=True)
        else:
            return queryset

    def search_first_product(self, queryset, name, value):
        if value > 0:
            return queryset.filter(service_id__exact=value)
        elif value == -1:
            return queryset.filter(service_id__isnull=True)
        else:
            return queryset

    def search_resource(self, queryset, name, value):
        return queryset.filter(Q(resource_name__icontains=value) | Q(manage_ip__icontains=value))

    class Meta:
        model = Resource
        fields = ['resource_name', "resource_type", "service_id", "server_purpose"]


class ResourceUserFilter(django_filters.rest_framework.FilterSet):
    """
    资源过滤类
    """

    user_name = django_filters.CharFilter(method="search_user_name")
    resource = django_filters.NumberFilter(method="search_resource")
    belong_user = django_filters.NumberFilter(method="search_belong_user")

    def search_resource(self, queryset, name, value):
        return queryset.filter(resource__exact=value)

    def search_user_name(self, queryset, name, value):
        return queryset.filter(user_name__exact=value)

    def search_belong_user(self, queryset, name, value):
        return queryset.filter(belong_user__exact=value)

    class Meta:
        model = ResourceUser
        fields = ['user_name', "resource", "belong_user"]
