import django_filters
from .models import WorkOrderTaskFlow


class WorkOrderTaskFlowFilter(django_filters.rest_framework.FilterSet):
    """
        资源过滤类
    """
    flow_name = django_filters.CharFilter(method='search_flow_name')
    flow_type = django_filters.ChoiceFilter(choices=WorkOrderTaskFlow.FLOW_TYPE_CHOICE)

    def search_flow_name(self, queryset, name, value):
        return queryset.filter(flow_name__exact=value)

    def search_flow_type(self, queryset, name, value):
        return queryset.filter(flow_type__exact=int(value))


    class Meta:
        model = WorkOrderTaskFlow
        fields = ['flow_name', "flow_type"]


# class ResourceUserFilter(django_filters.rest_framework.FilterSet):
#     """
#     资源过滤类
#     """
#
#     user_name = django_filters.CharFilter(method="search_user_name")
#     belong_resource = django_filters.NumberFilter(method="search_belong_resource")
#
#     def search_user_name(self, queryset, name, value):
#         return queryset.filter(user_name__exact=value)
#
#     def search_belong_resource(self, queryset, name, value):
#         return queryset.filter(belong_resource__exact=value)
#
#     class Meta:
#         model = ResourceUser
#         fields = ['user_name', "belong_resource"]
