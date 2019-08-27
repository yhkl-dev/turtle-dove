import django_filters
from .models import Tasks, AdHocTasks

class TasksFilter(django_filters.rest_framework.FilterSet):
    """
    任务过滤类
    """
    name  = django_filters.CharFilter(method='search_task_name')
    status = django_filters.CharFilter(method='search_task_status')

    def search_task_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    def search_task_status(self, queryset, name, value):
        return queryset.filter(status__exact=value)

    class Meta:
        model = Tasks
        fields = ['name', 'status']


class AdHocTasksFilter(django_filters.rest_framework.FilterSet):
    """
    任务过滤类
    """
    name  = django_filters.CharFilter(method='search_task_name')
    status = django_filters.CharFilter(method='search_task_status')

    def search_task_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    def search_task_status(self, queryset, name, value):
        return queryset.filter(status__exact=value)

    class Meta:
        model = AdHocTasks
        fields = ['name', 'status']