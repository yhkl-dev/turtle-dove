from rest_framework import viewsets, status
from rest_framework.response import Response
from TurtleDove.paginations import Pagination
from .serializers import ResourceUserSerializer, ResourceSerializer, ResourceTypeSerializer
from .models import ResourceUser, Resource, ResourceType
from .filters import ResourcesFilter, ResourceUserFilter


class ResourceTypeViewset(viewsets.ModelViewSet):
    """
            retrieve:
            返回指定资源类型信息

            list:
            返回资源类型列表

            update:
            更新资源类型信息

            destroy:
            删除资源类型记录

            create:
            创建资源类型

            partial_update:
            更新部分字段
    """

    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    pagination_class = Pagination


class ResourceViewset(viewsets.ModelViewSet):

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    pagination_class = Pagination
    filter_class = ResourcesFilter
    filter_fields = ("resource_name", "resource_type", "service_id", "server_purpose")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        resource_users_queryset = ResourceUser.objects.filter(belong_resource__exact=instance)
        for resource_user_obj in resource_users_queryset:
            resource_user_obj.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResourceUserViewset(viewsets.ModelViewSet):

    queryset = ResourceUser.objects.all()
    serializer_class = ResourceUserSerializer
    pagination_class = Pagination

    filter_class = ResourceUserFilter
    filter_fields = ('user_name', "belong_resource" )