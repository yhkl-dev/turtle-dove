import json
import os

from django.db.models import Q
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response

from turtle_dove.paginations import Pagination
from turtle_dove.settings import BASE_DIR
from .filters import WorkOrderTaskFilter
from .models import (WorkOrderTask,
                     WorkOrderOperation,
                     TemplateWorkOrderTaskFlow,
                     TemplateWorkOrderTaskFlowItem,
                     TemplateWorkOrderFlowType,
                     TemplateWorkOrderType,
                     TemplateWorkOrderProject,
                     TemplateWorkOrderModel,
                     WorkOrderStatusCode,
                     WorkOrderTaskFlowItem,
                     WorkOrderFlowType,
                     WorkOrderModel)
from .serializers import (WorkOrderOperationSerializer,
                          TemplateWorkOrderTaskFlowItemSerializer,
                          WorkOrderTaskSerializer,
                          TemplateWorkOrderTaskFlowSerializer,
                          TemplateWorkOrderFlowTypeSerializer,
                          TemplateWorkOrderTypeSerializer,
                          TemplateWorkOrderProjectSerializer,
                          TemplateWorkOrderModelSerializer,
                          WorkOrderStatusCodeSerializer)


def download_work_file(request):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
        print('下载 {} 完成'.format(file_name))

    if request.method == 'GET':
        file_name = request.GET['file_name']
        the_file_name = BASE_DIR + '/' + file_name
        if not os.path.exists(the_file_name):
            return HttpResponse('file not found', status.HTTP_404_NOT_FOUND)
            # raise IOError("file not found!")
        try:
            response = StreamingHttpResponse(file_iterator(the_file_name))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename={}".format(file_name)
            return response
        except Exception as e:
            return HttpResponse(json.dumps({"success": False, "error": u"下载文件失败"}), status=500,
                                content_type="text/json")


class LineChartViewSet(viewsets.ViewSet, mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        count_sql = '''
            select id, model_name, GROUP_CONCAT(id) id_list from work_order_model  GROUP BY model_name
        '''
        queryset = WorkOrderModel.objects.raw(count_sql)

        date_sql = '''
            SELECT id, DATE_SUB( CURDATE( ), INTERVAL date_sum.id DAY ) AS date FROM date_sum ORDER BY id desc 
        '''
        date_queryset = WorkOrderTask.objects.raw(date_sql)
        data = {}
        temp_list = []
        for n in date_queryset:
            temp_list.append(n.date)

        data.update(date_list=temp_list)

        count_data = []
        for q in queryset:
            sql = '''
                SELECT
                    b.id,
                    b.date,
                    c.total 
                FROM
                    ( SELECT id, DATE_SUB( CURDATE( ), INTERVAL date_sum.id DAY ) AS date FROM date_sum ) b
                    LEFT JOIN (SELECT count( * ) total, DATE( create_time ) x FROM work_order_task wot where order_model_id in ({}) GROUP BY DATE( create_time )) c on b.date = c.x
                    ORDER BY b.date 
                    
            '''.format(q.id_list)
            queryset_a = WorkOrderModel.objects.raw(sql)
            value_list = []
            for m in queryset_a:
                value_list.append(m.total if m.total else 0)
            current_data = {
                'name': q.model_name,
                'value_list': value_list
            }
            count_data.append(current_data)
        data.update(count_data_dict=count_data)

        sql = """
            SELECT
              b.id,
                b.date,
                a.total 
            FROM
                ( SELECT id, DATE_SUB( CURDATE( ), INTERVAL date_sum.id DAY ) AS date FROM date_sum ) b
                LEFT JOIN ( SELECT count( * ) total, DATE( create_time ) x FROM work_order_task wot GROUP BY DATE( create_time ) ) a ON b.date = a.x
            ORDER BY b.date 
        """
        queryset_total = WorkOrderModel.objects.raw(sql)
        total_data_list = []
        for x in queryset_total:
            total_data_list.append(x.total if x.total else 0)
        data.update(total_data_list=total_data_list)

        return Response(data, status=status.HTTP_200_OK)


class LineChartDataViewSet(viewsets.ViewSet, mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        name_data = []
        value_data = []
        sql = """
            SELECT
              b.id,
                b.date,
                a.total 
            FROM
                ( SELECT id, DATE_SUB( CURDATE( ), INTERVAL date_sum.id DAY ) AS date FROM date_sum ) b
                LEFT JOIN ( SELECT count( * ) total, DATE( create_time ) x FROM work_order_task wot GROUP BY DATE( create_time ) ) a ON b.date = a.x
            ORDER BY b.date 
        """
        queryset = WorkOrderModel.objects.raw(sql)
        for q in queryset:
            # info = {
            #     "name": q.date,
            #     "total_value": q.total
            # }
            value = q.total if q.total else 0
            name_data.append(q.date)
            value_data.append(value)
        data = {
            "name_data": name_data,
            "value_data": value_data
        }
        return Response(data, status=status.HTTP_200_OK)


class WorkOrderHistCountCheckByProductViewSet(viewsets.ViewSet,
                                              mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        id = request.GET.get('id')
        data = []
        sql = """
             SELECT
                wot.id,
                count( wom.model_name ) counts,
                wom.model_name 
            FROM
                work_order_task wot,
                work_order_model wom 
            WHERE
                wot.order_model_id = wom.id 
                and wot.order_products_id = {}
            GROUP BY
                wom.model_name
        """.format(id)
        queryset = WorkOrderModel.objects.raw(sql)
        for q in queryset:
            info = {
                "name": q.model_name,
                "value": q.counts
            }
            data.append(info)
        return Response(data, status=status.HTTP_200_OK)


class WorkOrderHistoryCountViewSet(viewsets.ViewSet, mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        data = []
        if user.username == 'admin':
            sql = """
                 SELECT
                        wot.id,
                        count( wom.model_name ) counts,
                        wom.model_name 
                    FROM
                        work_order_task wot,
                        work_order_model wom 
                    WHERE
                        wot.order_model_id = wom.id 
                    GROUP BY
                        wom.model_name
            """
        else:
            sql = """
                SELECT
                       wot.id,
                       count( wom.model_name ) counts,
                       wom.model_name 
                   FROM
                       work_order_task wot,
                       work_order_model wom 
                   WHERE
                       wot.order_model_id = wom.id 
                       and wot.created_user_id = '{}'
                   GROUP BY
                       wom.model_name
           """.format(user.id)
        queryset = WorkOrderModel.objects.raw(sql)
        for q in queryset:
            info = {
                "name": q.model_name,
                "value": q.counts
            }
            data.append(info)
        return Response(data, status=status.HTTP_200_OK)


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
    '''
        工单任务流程项
    '''

    queryset = TemplateWorkOrderTaskFlowItem.objects.all()
    serializer_class = TemplateWorkOrderTaskFlowItemSerializer
    pagination_class = Pagination


class TemplateWorkOrderFlowTypeViewset(viewsets.ModelViewSet):
    '''
        工单流程类型
    '''

    queryset = TemplateWorkOrderFlowType.objects.all()
    serializer_class = TemplateWorkOrderFlowTypeSerializer
    pagination_class = Pagination


class TemplateWorkOrderTypeViewset(viewsets.ModelViewSet):
    '''
        工单类型
    '''

    queryset = TemplateWorkOrderType.objects.all()
    serializer_class = TemplateWorkOrderTypeSerializer
    pagination_class = Pagination


class TemplateWorkOrderProjectViewset(viewsets.ModelViewSet):
    '''
        项目
    '''

    queryset = TemplateWorkOrderProject.objects.all()
    serializer_class = TemplateWorkOrderProjectSerializer
    pagination_class = Pagination


class WorkOrderTaskStatusCodeViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = WorkOrderStatusCode.objects.filter(
        status_belong_table__exact='work_order_task')
    serializer_class = WorkOrderStatusCodeSerializer
    pagination_class = None


class WorkOrderTaskOperationStatusCodeViewset(viewsets.ReadOnlyModelViewSet):
    queryset = WorkOrderStatusCode.objects.filter(
        status_belong_table__exact='work_order_operation')
    serializer_class = WorkOrderStatusCodeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None


class WorkOrderTaskViewset(viewsets.ModelViewSet):
    queryset = WorkOrderTask.objects.filter(~Q(order_status__in=[10, 11, 12]))
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination
    filter_class = WorkOrderTaskFilter
    filter_fields = ('order_task_id', 'order_title', 'template_order_model', 'create_time')

    def get_queryset(self):
        user = self.request.user
        queryset = super(WorkOrderTaskViewset, self).get_queryset()
        return queryset.filter(created_user=user)


class WorkOrderTaskHistoryViewset(viewsets.ModelViewSet):
    queryset = WorkOrderTask.objects.filter(order_status__in=[10, 11, 12])
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination
    filter_class = WorkOrderTaskFilter
    filter_fields = ('order_task_id', 'order_title', 'template_order_model', 'create_time')

    def get_queryset(self):
        user = self.request.user
        queryset = super(WorkOrderTaskHistoryViewset, self).get_queryset()
        if user.username == 'admin':
            return queryset
        else:
            return queryset.filter(created_user=user)


class WorkOrderTaskExecHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = WorkOrderTask.objects.filter(order_status__in=[10, 11, 12])
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination
    filter_class = WorkOrderTaskFilter
    filter_fields = ('order_task_id', 'order_title', 'template_order_model', 'create_time')

    def get_queryset(self):
        user = self.request.user
        sql = '''
            SELECT
                wot.id
            FROM
                work_order_task wot,
                work_order_model wom,
                work_order_flow_type woft,
                work_order_flow wof,
                work_order_flow_item wofi 
            WHERE
                wot.order_model_id = wom.id 
                AND wom.order_flow_type_id = woft.id 
                AND woft.task_exec_flow_id = wof.id 
                AND wof.id = wofi.belong_flow_id 
                AND wot.order_status IN ( 10, 11, 12 ) 
                and wofi.exec_user_id = '{}'
        '''.format(user.id)
        # queryset = super(WorkOrderTaskHistoryViewset, self).get_queryset()
        query_list = WorkOrderTask.objects.raw(sql)
        id_list = []
        for q in query_list:
            id_list.append(q.id)
        queryset = WorkOrderTask.objects.filter(id__in=id_list).order_by('-update_time')
        return queryset


class WorkOrderTaskAuditHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = WorkOrderTask.objects.filter(order_status__in=[10, 11, 12])
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination
    filter_class = WorkOrderTaskFilter
    filter_fields = ('order_task_id', 'order_title', 'template_order_model', 'create_time')

    def get_queryset(self):
        user = self.request.user
        sql = '''
            SELECT
                wot.id
            FROM
                work_order_task wot,
                work_order_model wom,
                work_order_flow_type woft,
                work_order_flow wof,
                work_order_flow_item wofi 
            WHERE
                wot.order_model_id = wom.id 
                AND wom.order_flow_type_id = woft.id 
                AND woft.task_audit_flow_id = wof.id 
                AND wof.id = wofi.belong_flow_id 
                AND wot.order_status IN ( 10, 11, 12 ) 
                and wofi.exec_user_id = '{}'
        '''.format(user.id)
        # queryset = super(WorkOrderTaskHistoryViewset, self).get_queryset()
        query_list = WorkOrderTask.objects.raw(sql)
        id_list = []
        for q in query_list:
            id_list.append(q.id)
        queryset = WorkOrderTask.objects.filter(id__in=id_list).order_by('-update_time')
        return queryset


class AuditWorkOrderTaskListViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        return WorkOrderTask.objects.filter(
            Q(current_audit_user=user) & Q(order_status=2)).order_by('-update_time')

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
                work_order_task_obj_list_queryset = WorkOrderTask.objects.filter(
                    Q(order_model=work_order_model_obj) & Q(order_status__in=[2, 6, 7])).order_by('-update_time')
                for q in work_order_task_obj_list_queryset:
                    if q not in work_order_task_list:
                        work_order_task_list.append(q)
            except Exception:
                continue
        return work_order_task_list


class ExecWorkOrderTaskListViewset(viewsets.ReadOnlyModelViewSet, ):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = WorkOrderTaskSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        return WorkOrderTask.objects.filter(
            Q(current_exec_user=user) & Q(order_status__in=[3, 4, 5])).order_by('-update_time')

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
                work_order_task_obj_list = WorkOrderTask.objects.filter(
                    Q(order_model=work_order_model_obj) & Q(order_status__in=[3, 4, 5, 6, 8])).order_by('-update_time')
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


class WorkOrderOperationViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = WorkOrderOperation.objects.all()
    serializer_class = WorkOrderOperationSerializer
    pagination_class = Pagination
    error_message = ''

    def create(self, request, *args, **kwargs):
        status_code = int(request.data.get('ops_status'))
        work_order_task_pk = request.data.get('work_order')

        if self._change_work_order_task_status(status_code, work_order_task_pk):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": self.error_message}, status=status.HTTP_400_BAD_REQUEST)

    def _get_audit_flow(self, instance) -> list:
        return instance.order_model.order_flow_type.task_audit_flow.belong_flow.all().order_by("exec_order")

    def _get_exec_flow(self, instance) -> list:
        return instance.order_model.order_flow_type.task_exec_flow.belong_flow.all().order_by("exec_order")

    def send_message_to_user(self, user, **kwargs):
        pass

    def _change_work_order_task_status(self, operation_code: int, work_order_pk: int) -> bool:
        current_operation_user = self.request.user
        work_order_task_obj = WorkOrderTask.objects.get(pk=work_order_pk)
        work_order_audit_flow = list(self._get_audit_flow(instance=work_order_task_obj))
        work_order_exec_flow = list(self._get_exec_flow(instance=work_order_task_obj))
        if operation_code == 1 and current_operation_user == work_order_task_obj.created_user:
            if work_order_task_obj.order_status == 1:
                work_order_task_obj.order_status = 2
                current_audit_flow_item_obj = work_order_audit_flow[0]
                work_order_task_obj.current_audit_user = current_audit_flow_item_obj.exec_user
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
            if current_operation_user == work_order_audit_flow[-1].exec_user:
                if work_order_task_obj.order_status != 3:
                    work_order_task_obj.order_status = 3
                    current_audit_flow_item_obj = work_order_audit_flow[-1]
                    current_audit_flow_item_obj.ops_status = 2

                    current_exec_flow_item_obj = work_order_exec_flow[0]

                    work_order_task_obj.current_exec_user = current_exec_flow_item_obj.exec_user
                    current_audit_flow_item_obj.save()
                    work_order_task_obj.save()
                    return True
                else:
                    self.error_message = '不可重复审核通过'
                    return False
            else:
                # 如果当前审核用户不是审核列表的最后一个人， 审核通过 转至 下一个审核人处理
                work_order_task_obj.order_status = 2
                work_order_audit_flow_user = [q.exec_user for q in work_order_audit_flow]
                current_ptr = work_order_audit_flow_user.index(current_operation_user)
                next_ptr = current_ptr + 1
                current_audit_flow = work_order_audit_flow[current_ptr]
                current_audit_flow.ops_status = 2
                current_audit_flow.save()
                next_audit_flow = work_order_audit_flow[next_ptr]
                work_order_task_obj.current_audit_user = next_audit_flow.exec_user
                work_order_task_obj.save()
                return True

        if operation_code == 3 and current_operation_user == work_order_task_obj.current_audit_user:
            work_order_task_obj.order_status = 7
            work_order_audit_flow_user = [q.exec_user for q in work_order_audit_flow]
            current_ptr = work_order_audit_flow_user.index(current_operation_user)
            current_audit_flow = work_order_audit_flow[current_ptr]
            current_audit_flow.ops_status = 3
            current_audit_flow.save()
            # 审核不通过 -> 审核驳回,等待用户确认
            work_order_task_obj.save()
            return True
        # 4 这个位置逻辑有问题， 已经写好的流程，转发的时候， 如果不在列表里面 相关的用户可能收不到 这里可能需要修改表结构了
        if operation_code == 4 and current_operation_user == work_order_task_obj.current_audit_user:
            work_order_task_obj.order_status = 2
            # 审核转发 -> 审核中

            work_order_task_obj.save()
            return True
        if operation_code == 5 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status = 4
            # 确认执行 -> 执行人执行中

            work_order_exec_flow_user = [q.exec_user for q in work_order_exec_flow]
            current_ptr = work_order_exec_flow_user.index(current_operation_user)
            current_audit_flow_item = work_order_exec_flow[current_ptr]
            current_audit_flow_item.ops_status = 5
            current_audit_flow_item.save()
            work_order_task_obj.save()
            return True
        if operation_code == 6 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status = 6
            # 这个代码是给 执行者 使用的， 如果执行不通过， 用户输入6 ， 状态变为 执行完成， 申请用户确认中
            # 执行确认不通过 -> 执行驳回,等待用户确认
            work_order_exec_flow_user = [q.exec_user for q in work_order_exec_flow]
            current_ptr = work_order_exec_flow_user.index(current_operation_user)
            current_audit_flow_item = work_order_exec_flow[current_ptr]
            current_audit_flow_item.ops_status = 6
            current_audit_flow_item.save()
            work_order_task_obj.save()
            return True
        if operation_code == 7 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status = 5
            work_order_exec_flow_user = [q.exec_user for q in work_order_exec_flow]
            current_ptr = work_order_exec_flow_user.index(current_operation_user)
            current_audit_flow_item = work_order_exec_flow[current_ptr]
            current_audit_flow_item.ops_status = 7
            current_audit_flow_item.save()
            # 延期执行 -> 执行人延期执行中
            work_order_task_obj.save()
            return True
        if operation_code == 8 and current_operation_user == work_order_task_obj.current_exec_user:
            if current_operation_user == work_order_exec_flow[-1].exec_user:
                # 执行完成 -> 执行完成,用户确认中
                if work_order_task_obj.order_status in [6, 8, 9, 11, 12, 13, 14]:
                    self.error_message = '当前不允许此操作'
                    return False
                work_order_task_obj.order_status = 6
                work_order_exec_flow_user = [q.exec_user for q in work_order_exec_flow]
                current_ptr = work_order_exec_flow_user.index(current_operation_user)
                current_exec_flow_item = work_order_exec_flow[current_ptr]
                current_exec_flow_item.ops_status = 8

                # work_order_task_obj.save()
                if self.request.data.get('ops_reply_content') is None:
                    self.error_message = '执行结果不能为空'
                    return False
                else:
                    work_order_task_obj.order_result = self.request.data.get('ops_reply_content')
                current_exec_flow_item.save()
                work_order_task_obj.save()
                return True
            else:
                work_order_task_obj.order_status = 3
                # 当前执行人完成， 发给下一个执行人， 等待下一个执行人确认
                work_order_exec_flow_user = [q.exec_user for q in work_order_exec_flow]
                current_ptr = work_order_exec_flow_user.index(current_operation_user)
                next_ptr = current_ptr + 1
                current_exec_flow_item = work_order_exec_flow[current_ptr]
                current_exec_flow_item.ops_status = 8
                current_exec_flow_item.save()
                next_exec_flow_item = work_order_exec_flow[next_ptr]
                work_order_task_obj.current_exec_user = next_exec_flow_item.exec_user
                # 执行完成需要给用户发消息确认 同时将结果添加至工单任务表的结果中
                work_order_task_obj.save()
                return True
        # 这个有问题，先不用
        if operation_code == 9 and current_operation_user == work_order_task_obj.current_exec_user:
            work_order_task_obj.order_status = 3
            # 执行转发 -> 执行人确认中
            work_order_task_obj.save()
            return True
        if operation_code == 10 and current_operation_user == work_order_task_obj.created_user:
            work_order_task_obj.order_status = 9
            # 用户确认不通过 -> 用户确认不通过,等待执行重做
            # 给执行用户发送消息， 告知执行结果不通过， 流程返回至 第一执行人
            work_order_task_obj.current_exec_user = work_order_exec_flow[0].exec_user
            for q in work_order_exec_flow:
                q.ops_status = None
                q.save()
            work_order_task_obj.save()
            return True
        if operation_code == 11 and current_operation_user == work_order_task_obj.created_user:
            if work_order_task_obj.order_status == 6:
                work_order_task_obj.order_status = 10
                # 执行完成,用户确认中 -> 关闭 -> 完成关闭
                work_order_task_obj.save()
                return True
            if work_order_task_obj.order_status == 7 or work_order_task_obj.order_status == 8:
                work_order_task_obj.order_status = 11
                # 审核驳回,等待用户确认 -> 关闭 > 驳回关闭
                work_order_task_obj.save()
                return True
        if operation_code == 12 and current_operation_user == work_order_task_obj.created_user:
            if work_order_task_obj.order_status == 9:
                # 重走流程 -> 如果是 用户确认不通过,等待执行重做
                work_order_task_obj.order_status = 3
                work_order_task_obj.current_exec_user = work_order_exec_flow[0].exec_user
                for q in work_order_exec_flow:
                    q.ops_status = None
                    q.save()
                work_order_task_obj.save()
                return True
            if work_order_task_obj.order_status == 7:
                work_order_task_obj.order_status = 2
                work_order_task_obj.current_audit_user = work_order_audit_flow[0].exec_user
                for q in work_order_audit_flow:
                    q.ops_status = None
                    q.save()
                # 如果工单状态 为审核驳回， 则重新进行审核
                work_order_task_obj.save()
                return True
        if operation_code == 13 and current_operation_user == work_order_task_obj.created_user:
            # 重新编辑工单的条件为 工单必须处于待提交 、 审核驳回， 执行驳回 这几种状态
            if work_order_task_obj.order_status in [1, 7, 8]:
                work_order_task_obj.order_status = 1
                work_order_task_obj.current_audit_user = work_order_audit_flow[0].exec_user
                work_order_task_obj.current_exec_user = None
                work_order_task_obj.save()
                return True
        if operation_code == 14 and current_operation_user == work_order_task_obj.created_user:
            # 用户确认后 再向工单表中插入相关用户数据 比如 审核， 执行等动作
            # 撤回工单的条件为，当前审核流程 第一审核用户未审核， 也就是说 current_audit_user 为空
            if work_order_task_obj.order_status == 2 and work_order_audit_flow[0].ops_status is None:
                work_order_task_obj.order_status = 12  # 撤销关闭
                work_order_task_obj.current_audit_user = None
                work_order_task_obj.save()
                return True
        if operation_code == 15:
            return True
