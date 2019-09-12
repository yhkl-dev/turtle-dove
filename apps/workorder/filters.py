import django_filters
from django.db.models import Q
from .models import WorkOrderTaskFlow, WorkOrderTask
import uuid


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


class WorkOrderTaskFilter(django_filters.rest_framework.FilterSet):
    """
    资源过滤类
    """

    order_task_id = django_filters.UUIDFilter(method="search_order_task_id")
    order_title = django_filters.CharFilter(method="search_order_title")
    template_order_model = django_filters.NumberFilter(method="search_template_order_model")

    def search_order_task_id(self, queryset, name, value):
        return queryset.filter(order_task_id__exact=value)

    def search_order_title(self, queryset, name, value):
        return queryset.filter(order_title__icontains=value)

    def search_template_order_model(self, queryset, name, value):
        return queryset.filter(template_order_model__exact=value)

    class Meta:
        model = WorkOrderTask
        fields = ['order_task_id', 'order_title', 'template_order_model']
        # fields = [ 'order_title', 'template_order_model']
