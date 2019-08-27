from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .filter import TasksFilter, AdHocTasksFilter
from .serializers import TasksSerializer, AdHocTasksSerializer
from .models import Tasks, AdHocTasks
from .tasks import run_play_book, run_adhoc_task
import json

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class TasksViewset(viewsets.ModelViewSet, mixins.UpdateModelMixin):
    """
    create:
    创建任务
    list:
    获取任务列表
    retrieve:
    获取任务信息
    update:
    执行任务
    """
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tasks.objects.filter(is_visible__exact='Y')
    serializer_class = TasksSerializer
    pagination_class = Pagination
    filter_class = TasksFilter
    filter_fields = ('name', 'status')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    ordering_fields = ('id',)

    def partial_update(self, request, *args, **kwargs):
         pk = int(kwargs.get("pk"))
         data = request.data
         print(data.get('status'))
         task = Tasks.objects.get(pk=pk)
         detail_result = {
             'data': '数据正在处理，请稍候'
         }
         # data['detail_result'] = json.dumps(detail_result, indent=4)
         if data.get('is_visible') == "N":
             Tasks.objects.filter(pk=pk).update(is_visible=data.get('is_visible'))
             return Response(status=status.HTTP_204_NO_CONTENT)
         if data.get('status') == 'R':
             Tasks.objects.filter(pk=pk).update(status=data.get('status'),exec_time=timezone.now(),detail_result=json.dumps(detail_result, indent=4) )
             run_play_book.apply_async((pk, task.playbook.path))
             return Response(status=status.HTTP_204_NO_CONTENT)


class AdHocTasksViewset(viewsets.ModelViewSet, mixins.UpdateModelMixin):
    """
    create:
    创建Ad-hoc任务
    list:
    获取Ad-hoc任务列表
    retrieve:
    获取Ad-hoc任务信息
    update:
    执行Ad-hoc任务
    """
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AdHocTasks.objects.filter(is_visible__exact='Y')
    serializer_class = AdHocTasksSerializer
    pagination_class = Pagination
    filter_class = AdHocTasksFilter
    filter_fields = ('name', 'status')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    ordering_fields = ('id',)

    def partial_update(self, request, *args, **kwargs):
         pk = int(kwargs.get("pk"))
         data = request.data
         print(data)
         task = AdHocTasks.objects.get(pk=pk)
         detail_result = {
             'data': '数据正在处理，请稍候'
         }
         if data.get('is_visible') == 'N':
             AdHocTasks.objects.filter(pk=pk).update(is_visible=data.get('is_visible'))
             return Response(status=status.HTTP_204_NO_CONTENT)

         if data.get('status') == "R":
             c = task.exec_host
             d = c.split(',')
             AdHocTasks.objects.filter(pk=pk).update(status=data.get('status'),exec_time=timezone.now(),detail_result=json.dumps(detail_result, indent=4) )
             run_adhoc_task.apply_async((pk,tuple(d), task.model_name, task.model_args))
             return Response(status=status.HTTP_204_NO_CONTENT)
