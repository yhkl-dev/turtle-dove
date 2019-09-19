from .models import ProjectConfigure, Project
from .serializers import ProjectSerializer, ProjectConfigureSerializer
from rest_framework import viewsets, mixins, permissions


class ProjectViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin):

    """
        list:
            查询
        create:
            创建
        update:
            更新

    """

    permission_classes =  (permissions.IsAuthenticated,)
    queryset = Project.objects.filter(is_deleted=0)
    serializer_class = ProjectSerializer


class ProjectConfigureViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin):

    """
        create:
            查询
        update:
            更新
        delete:
            删除
    """
    queryset = ProjectConfigure.objects.all()
    serializer_class = ProjectConfigureSerializer
