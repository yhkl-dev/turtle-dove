from .models import (WorkOrderTask,
                     WorkOrderOperation,
                     TemplateWorkOrderTaskFlow,
                     TemplateWorkOrderTaskFlowItem,
                     TemplateWorkOrderFlowType,
                     TemplateWorkOrderType,
                     TemplateWorkOrderProject,
                     TemplateWorkOrderModel,
                     WorkOrderModel,
                     WorkOrderStatusCode,
                     WorkOrderTaskFlow,
                     WorkOrderTaskFlowItem,
                     WorkOrderFlowType,
                     WorkOrderType,
                     WorkOrderProject,
                     )
from .serializers import (WorkOrderOperationSerializer,
                          TemplateWorkOrderTaskFlowItemSerializer,
                          TemplateWorkOrderFlowTypeSerializer,
                          WorkOrderTaskSerializer,
                          TemplateWorkOrderTaskFlowSerializer,
                          TemplateWorkOrderTypeSerializer,
                          TemplateWorkOrderProjectSerializer,
                          TemplateWorkOrderModelSerializer)
from rest_framework import viewsets, status, permissions, mixins
from TurtleDove.paginations import Pagination
from .filters import WorkOrderTaskFlowFilter
from rest_framework.response import Response


class TemplateWorkOrderTaskFlowViewset(viewsets.ModelViewSet):
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

    queryset = TemplateWorkOrderTaskFlow.objects.all()
    serializer_class = TemplateWorkOrderTaskFlowSerializer
    pagination_class = Pagination
    # filter_class = WorkOrderTaskFlowFilter
    # filter_fields = ('flow_name', "flow_type")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        work_flow_item_queryset = TemplateWorkOrderTaskFlowItem.objects.filter(belong_flow__exact=instance)
        for work_flow_item_obj in work_flow_item_queryset:
            work_flow_item_obj.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TemplateWorkOrderTaskFlowItemViewset(viewsets.ModelViewSet):

    queryset = TemplateWorkOrderTaskFlowItem.objects.all()
    serializer_class = TemplateWorkOrderTaskFlowItemSerializer
    pagination_class = Pagination


class TemplateWorkOrderFlowTypeViewset(viewsets.ModelViewSet):

    queryset = TemplateWorkOrderFlowType.objects.all()
    serializer_class = TemplateWorkOrderFlowTypeSerializer
    pagination_class = Pagination


class TemplateWorkOrderTypeViewset(viewsets.ModelViewSet):

    queryset = TemplateWorkOrderType.objects.all()
    serializer_class = TemplateWorkOrderTypeSerializer
    pagination_class = Pagination


class TemplateWorkOrderProjectViewset(viewsets.ModelViewSet):

    queryset = TemplateWorkOrderProject.objects.all()
    serializer_class = TemplateWorkOrderProjectSerializer
    pagination_class = Pagination


class WorkOrderTaskStatusCodeViewset(viewsets.ViewSet, mixins.ListModelMixin):

    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        data= {
            'code': WorkOrderStatusCode.objects.filter(
            status_belong_table__exact='work_order_task').values_list(
            'status_code', 'status_name')
        }
        return Response(data, status=status.HTTP_200_OK)


class WorkOrderTaskOperationStatusCodeViewset(viewsets.ViewSet, mixins.ListModelMixin):

    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        data= {
            'code': WorkOrderStatusCode.objects.filter(
            status_belong_table__exact='work_order_operation').values_list(
            'status_code', 'status_name')
        }
        return Response(data, status=status.HTTP_200_OK)


class WorkOrderTaskViewset(viewsets.ModelViewSet):

    queryset = WorkOrderTask.objects.all()
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        queryset = super(WorkOrderTaskViewset, self).get_queryset()
        return queryset.filter(created_user=user)



class AuditWorkOrderTaskListViewset(viewsets.ReadOnlyModelViewSet):

    # queryset = get_audit_work_order_list()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        queryset = self.get_audit_work_order_list(user)
        return queryset

    def get_audit_work_order_list(self, user):
        # user = self.request.user
        # 首先根据用户查询 work_order_flow_item 里面有没有当前用户的 item
        work_order_flow_item_queryset = WorkOrderTaskFlowItem.objects.filter(exec_user=user)  # 得到 item 列表

        work_flow_list = []
        for flow_item_obj in work_order_flow_item_queryset:
            work_flow_list.append(flow_item_obj.belong_flow)

        work_flow_type_list = []
        for work_flow_obj in work_flow_list:
            try:
                work_flow_type_obj = WorkOrderFlowType.objects.filter(task_audit_flow=work_flow_obj)
                for q in work_flow_type_obj:
                    if q not in work_flow_type_list:
                        work_flow_type_list.append(q)
            except WorkOrderFlowType.DoesNotExist:
                continue

        work_order_model_list = []
        for work_flow_type_obj in work_flow_type_list:
            try:
                work_order_model_obj_list = WorkOrderModel.objects.filter(order_flow_type=work_flow_type_obj)
                for q in work_order_model_obj_list:
                    if q not in work_order_model_list:
                        work_order_model_list.append(q)
            except Exception:
                continue

        work_order_task_list = []
        for work_order_model_obj in work_order_model_list:
            try:
                work_order_task_obj_list = WorkOrderTask.objects.filter(order_model=work_order_model_obj)
                for q in work_order_task_obj_list:
                    if q not in work_order_task_list:
                        work_order_task_list.append(q)
            except Exception:
                continue
        return work_order_task_list


class ExecWorkOrderTaskListViewset(viewsets.ReadOnlyModelViewSet, ):

    # queryset = get_audit_work_order_list()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        queryset = self.get_exect_work_order_list(user)
        return queryset

    def get_exect_work_order_list(self, user):
        # 首先根据用户查询 work_order_flow_item 里面有没有当前用户的 item
        work_order_flow_item_queryset = WorkOrderTaskFlowItem.objects.filter(exec_user=user)  # 得到 item 列表

        work_flow_list = []
        for flow_item_obj in work_order_flow_item_queryset:
            work_flow_list.append(flow_item_obj.belong_flow)

        work_flow_type_list = []
        for work_flow_obj in work_flow_list:
            try:
                work_flow_type_obj = WorkOrderFlowType.objects.filter(task_exec_flow=work_flow_obj)
                for q in work_flow_type_obj:
                    if q not in work_flow_type_list:
                        work_flow_type_list.append(q)
            except WorkOrderFlowType.DoesNotExist:
                continue
        work_order_model_list = []
        for work_flow_type_obj in work_flow_type_list:
            try:
                work_order_model_obj_list = WorkOrderModel.objects.filter(order_flow_type=work_flow_type_obj)
                for q in work_order_model_obj_list:
                    if q not in work_order_model_list:
                        work_order_model_list.append(q)
            except Exception:
                continue

        work_order_task_list = []
        for work_order_model_obj in work_order_model_list:
            try:
                work_order_task_obj_list = WorkOrderTask.objects.filter(order_model=work_order_model_obj)
                for q in work_order_task_obj_list:
                    if q not in work_order_task_list:
                        work_order_task_list.append(q)
            except Exception:
                continue
        return work_order_task_list


class TemplateWorkOrderModelViewset(viewsets.ModelViewSet):

    queryset = TemplateWorkOrderModel.objects.all()
    serializer_class = TemplateWorkOrderModelSerializer
    pagination_class = Pagination


class WorkOrderOperationViewset(viewsets.ModelViewSet):

    queryset = WorkOrderOperation.objects.all()
    serializer_class = WorkOrderOperationSerializer
    pagination_class = Pagination
    error_message = ''

    def create(self, request, *args, **kwargs):
        status_code = int(request.data.get('ops_status'))
        work_order_task_pk = request.data.get('work_order')
        print(work_order_task_pk)

        if self._change_work_order_task_status(status_code, work_order_task_pk):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": self.error_message}, status=status.HTTP_400_BAD_REQUEST)

    def _get_audit_flow(self, instance) -> list:
        # instance = WorkOrderTask.objects.get(pk=work_order_pk)
        audit_user_list = []
        queryset = instance.order_model.order_flow_type.task_audit_flow.belong_flow.all().order_by("exec_order")
        for q in queryset:
            audit_user_list.append(q.exec_user)
        print(audit_user_list)
        return audit_user_list

    def _get_exec_flow(self, instance) -> list:
        # instance = WorkOrderTask.objects.get(pk=work_order_pk)
        exec_user_list = []
        queryset = instance.order_model.order_flow_type.task_audit_flow.belong_flow.all().order_by("exec_order")
        for q in queryset:
            exec_user_list.append(q.exec_user)
        print(exec_user_list)
        return exec_user_list

    def send_message_to_user(self, user, **kwargs):
        pass


    def _change_work_order_task_status(self, operation_code:int, work_order_pk:int) -> bool:
        current_operation_user = self.request.user
        work_order_task_obj = WorkOrderTask.objects.get(pk=work_order_pk)
        work_order_audit_flow = list(self._get_audit_flow(instance=work_order_task_obj))
        work_order_exec_flow = list(self._get_exec_flow(instance=work_order_task_obj))
        if operation_code == 1:
            if work_order_task_obj.order_status == 1:
                work_order_task_obj.order_status=2
                work_order_task_obj.current_audit_user = work_order_audit_flow[0]
                work_order_task_obj.save()
                # 提交 -> 审核中
                return True
            else:
                self.error_message = '不允许重复提交'
                return False
        if operation_code == 2 and current_operation_user == work_order_task_obj.current_audit_user:
            # 这里其实分情况讨论
            # 如果当前执行用户是审核列表的最后一个人
            # 审核通过 -> 执行人确认 这里需要校验 当前工单的状态
            if current_operation_user == work_order_audit_flow[-1] :
                if work_order_task_obj.order_status != 3:
                    work_order_task_obj.order_status=3
                    work_order_task_obj.current_exec_user = work_order_exec_flow[0]
                    work_order_task_obj.save()
                    return True
                else:
                    self.error_message = '不可重复审核通过'
                    return False
            else:
                # 如果当前审核用户不是审核列表的最后一个人， 审核通过 转至 下一个审核人处理
                work_order_task_obj.order_status = 2
                work_order_task_obj.current_audit_user = work_order_audit_flow[work_order_audit_flow.index(current_operation_user) + 1]
                work_order_task_obj.save()
                return True
        if operation_code == 3 and current_operation_user == work_order_task_obj.current_audit_user:
            work_order_task_obj.order_status=7
            # 审核不通过 -> 审核驳回,等待用户确认
            work_order_task_obj.save()
            return True
        # 4 这个位置逻辑有问题， 已经写好的流程，转发的时候， 如果不在列表里面 相关的用户可能收不到 这里可能需要修改表结构了
        if operation_code == 4 and current_operation_user == work_order_task_obj.current_audit_user:
            work_order_task_obj.order_status=2
            # 审核转发 -> 审核中
            work_order_task_obj.save()
            return True
        if operation_code == 5 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status=4
            # 确认执行 -> 执行人执行中
            work_order_task_obj.save()
            return True
        if operation_code == 6 and current_operation_user == work_order_task_obj.current_exec_user :
            work_order_task_obj.order_status=8
            # 执行确认不通过 -> 执行驳回,等待用户确认
            work_order_task_obj.save()
            return True
        if operation_code == 7 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status=5
            # 延期执行 -> 执行人延期执行中
            work_order_task_obj.save()
            return True
        if operation_code == 8 and current_operation_user == work_order_task_obj.current_exec_user:
            if current_operation_user == work_order_exec_flow[-1]:
                # 执行完成 -> 执行完成,用户确认中
                work_order_task_obj.order_status=6
                if self.request.data.get('ops_reply_content') is None:
                    self.error_message = '执行结果不能为空'
                    return False
                else:
                    work_order_task_obj.order_result = self.request.data.get('ops_reply_content')
                    work_order_task_obj.save()
                    return True
            else:
                work_order_task_obj.order_status = 3
                # 当前执行人完成， 发给下一个执行人， 等待下一个执行人确认
                work_order_task_obj.current_exec_user = work_order_exec_flow[work_order_exec_flow.index(current_operation_user) + 1]
                # 执行完成需要给用户发消息确认 同时将结果添加至工单任务表的结果中
                work_order_task_obj.save()
                return True
        # 这个有问题，先不用
        if operation_code == 9 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status=3
            # 执行转发 -> 执行人确认中
            work_order_task_obj.save()
            return True
        if operation_code == 10 and current_operation_user == work_order_task_obj.created_user:
            work_order_task_obj.order_status=9
            # 用户确认不通过 -> 用户确认不通过,等待执行重做
            # 给执行用户发送消息， 告知执行结果不通过， 流程返回至 第一执行人
            work_order_task_obj.save()
            return True
        if operation_code == 11 and current_operation_user == work_order_task_obj.created_user:
            if work_order_task_obj.order_status == 6:
                work_order_task_obj.order_status=10
                # 执行完成,用户确认中 -> 关闭 -> 完成关闭
                work_order_task_obj.save()
                return True
            if work_order_task_obj.order_status == 7 or work_order_task_obj.order_status == 8:
                work_order_task_obj.order_status=11
                # 审核驳回,等待用户确认 -> 关闭 > 驳回关闭
                work_order_task_obj.save()
                return True
        if operation_code == 12 and current_operation_user == work_order_task_obj.created_user:
            if work_order_task_obj.order_status == 9:
                # 重走流程 -> 如果是 用户确认不通过,等待执行重做
                work_order_task_obj.order_status=3
                work_order_task_obj.current_exec_user = work_order_exec_flow[0]
                work_order_task_obj.save()
                return True
            if work_order_task_obj.order_status == 7 :
                work_order_task_obj.order_status=2
                work_order_task_obj.current_audit_user = work_order_audit_flow[0]
                # 如果工单状态 为审核驳回， 则重新进行审核
                work_order_task_obj.save()
                return True
        if operation_code == 13 and current_operation_user == work_order_task_obj.created_user:
            # 重新编辑工单的条件为 工单必须处于待提交 、 审核驳回， 执行驳回 这几种状态
            if work_order_task_obj.order_status in [1, 7 ,8 ]:
                work_order_task_obj.order_status=1
                work_order_task_obj.current_audit_user = work_order_audit_flow[0]
                work_order_task_obj.current_exec_user = None
                work_order_task_obj.save()
                return True
        if operation_code == 14 and current_operation_user == work_order_task_obj.created_user:
            # 用户确认后再向工单表中插入相关用户数据 比如 审核， 执行等动作
            # 撤回工单的条件为，当前审核流程 第一审核用户未审核， 也就是说 current_audit_user 为空
            if work_order_task_obj.order_status == 2 and work_order_task_obj.current_audit_user is None:
                work_order_task_obj.order_status=1
                work_order_task_obj.save()
                return True
        if operation_code == 15:
            return True
