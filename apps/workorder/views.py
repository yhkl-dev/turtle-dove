from .models import (WorkOrderTask,
                     WorkOrderOperation,
                     WorkOrderTaskFlow,
                     WorkOrderTaskFlowItem,
                     WorkOrderFlowType,
                     WorkOrderType,
                     WorkOrderProject,
                     WorkOrderModel)
from .serializers import (WorkOrderOperationSerializer,
                          WorkOrderTaskFlowItemSerializer,
                          WorkOrderFlowTypeSerializer,
                          WorkOrderTaskSerializer,
                          WorkOrderTaskFlowSerializer,
                          WorkOrderTypeSerializer,
                          WorkOrderProjectSerializer,
                          WorkOrderModelSerializer)
from rest_framework import viewsets, status
from TurtleDove.paginations import Pagination
from .filters import WorkOrderTaskFlowFilter
from rest_framework.response import Response


class WorkOrderTaskFlowViewset(viewsets.ModelViewSet):
    '''
        retrieve：
            返回指定工单工单流程信息

        list:
            返工单流程信息列表

        create:
            添加工单流程信息列表

        update:
            修改工单流程信息

        destroy:
            删除工单流程信息

        partial_update:
            更新工单流程信息部分字段
    '''

    queryset = WorkOrderTaskFlow.objects.all()
    serializer_class = WorkOrderTaskFlowSerializer
    pagination_class = Pagination
    filter_class = WorkOrderTaskFlowFilter
    filter_fields = ('flow_name', "flow_type")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        work_flow_item_queryset = WorkOrderTaskFlowItem.objects.filter(belong_flow__exact=instance)
        for work_flow_item_obj in work_flow_item_queryset:
            work_flow_item_obj.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkOrderTaskFlowItemViewset(viewsets.ModelViewSet):

    queryset = WorkOrderTaskFlowItem.objects.all()
    serializer_class = WorkOrderTaskFlowItemSerializer
    pagination_class = Pagination


class WorkOrderFlowTypeViewset(viewsets.ModelViewSet):

    queryset = WorkOrderFlowType.objects.all()
    serializer_class = WorkOrderFlowTypeSerializer
    pagination_class = Pagination


class WorkOrderTypeViewset(viewsets.ModelViewSet):

    queryset = WorkOrderType.objects.all()
    serializer_class = WorkOrderTypeSerializer
    pagination_class = Pagination


class WorkOrderProjectViewset(viewsets.ModelViewSet):

    queryset = WorkOrderProject.objects.all()
    serializer_class = WorkOrderProjectSerializer
    pagination_class = Pagination


class WorkOrderTaskViewset(viewsets.ModelViewSet):

    queryset = WorkOrderTask.objects.all()
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination


class WorkOrderModelViewset(viewsets.ModelViewSet):

    queryset = WorkOrderModel.objects.all()
    serializer_class = WorkOrderModelSerializer
    pagination_class = Pagination


class WorkOrderOperationViewset(viewsets.ModelViewSet):

    queryset = WorkOrderOperation.objects.all()
    serializer_class = WorkOrderOperationSerializer
    pagination_class = Pagination
