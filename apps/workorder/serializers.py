from rest_framework import serializers
from django.db.models import Q
from .models import (WorkOrderTask,
                     WorkOrderOperation,
                     WorkOrderTaskFlow,
                     WorkOrderTaskFlowItem,
                     WorkOrderFlowType,
                     WorkOrderType,
                     WorkOrderProject,
                     WorkOrderModel)


class WorkOrderTaskFlowItemSerializer(serializers.ModelSerializer):
    '''
        工单执行流程项序列化类
    '''

    def to_representation(self, instance):
        ret = super(WorkOrderTaskFlowItemSerializer, self).to_representation(instance)
        ret['belong_flow'] = instance.belong_flow.flow_name
        ret['exec_user'] = instance.exec_user.username
        return ret

    def validate(self, attrs):
        task_flow_queryset = WorkOrderTaskFlowItem.objects.filter(belong_flow__exact=attrs.get("belong_flow")).values('exec_order')
        c = [q.get('exec_order') for q in task_flow_queryset]
        if attrs.get("exec_order") in c:
            raise serializers.ValidationError('Duplicated exec_order number')
        else:
            return attrs

    class Meta:
        model = WorkOrderTaskFlowItem
        fields = "__all__"


class WorkOrderTaskFlowSerializer(serializers.ModelSerializer):

    '''
        工单执行流程序列化类
    '''

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="创建日期",
                                            read_only=True,
                                            help_text="创建日期")
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="修改日期",
                                            read_only=True,
                                            help_text="修改日期")

    def to_representation(self, instance):
        task_flow_item_queryset = WorkOrderTaskFlowItem.objects.filter(belong_flow__exact=instance).order_by('exec_order')
        flow_item_sets = []
        for q in task_flow_item_queryset:
            flow_item = {
                "id": q.id,
                "exec_order": q.exec_order,
                "flow_item_name": q.flow_item_name,
                "exec_user": q.exec_user.username
            }
            flow_item_sets.append(flow_item)
        ret = super(WorkOrderTaskFlowSerializer, self).to_representation(instance)
        ret['flow_type'] = instance.get_flow_type_display()
        ret['flow_item'] = flow_item_sets
        return ret

    class Meta:
        model = WorkOrderTaskFlow
        fields = '__all__'


class WorkOrderFlowTypeSerializer(serializers.ModelSerializer):

    '''
        工单执行流程类型序列化类
    '''

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="创建日期",
                                            read_only=True,
                                            help_text="创建日期")
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="修改日期",
                                            read_only=True,
                                            help_text="修改日期")

    def to_representation(self, instance):
        ret = super(WorkOrderFlowTypeSerializer, self).to_representation(instance)
        ret['flow_type_status'] = instance.get_flow_type_status_display()
        ret['task_exec_flow'] = instance.task_exec_flow.flow_name
        ret['task_audit_flow'] = instance.task_audit_flow.flow_name
        return ret


    class Meta:
        model = WorkOrderFlowType
        fields = "__all__"


class WorkOrderTypeSerializer(serializers.ModelSerializer):

    '''
        工单类型序列化类
    '''

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="创建日期",
                                            read_only=True,
                                            help_text="创建日期")
    change_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="修改日期",
                                            read_only=True,
                                            help_text="修改日期")

    def to_representation(self, instance):
        ret = super(WorkOrderTypeSerializer, self).to_representation(instance)
        ret['type_status'] = instance.get_type_status_display()
        return ret

    class Meta:
        model = WorkOrderType
        fields = "__all__"


class WorkOrderProjectSerializer(serializers.ModelSerializer):

    '''
        工单项目序列化类
    '''
    class Meta:
        model = WorkOrderProject
        fields = "__all__"


class WorkOrderModelSerializer(serializers.ModelSerializer):

    '''
        工单模板序列化类
    '''

    model_create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                                  label="创建日期",
                                                  read_only=True,
                                                  help_text="创建日期")

    def to_representation(self, instance):
        ret = super(WorkOrderModelSerializer,self).to_representation(instance)
        ret['order_type'] = instance.order_type.type_name
        ret['order_flow_type'] = instance.order_flow_type.flow_type_name
        return ret


    class Meta:
        model = WorkOrderModel
        fields = '__all__'


class WorkOrderTaskSerializer(serializers.ModelSerializer):

    '''
        工单任务序列化类
    '''

    order_task_id = serializers.UUIDField(read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="创建日期",
                                            read_only=True,
                                            help_text="创建日期")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="更新时间",
                                            read_only=True,
                                            help_text="更新时间")
    created_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    def get_user_info(self, user_obj):
        try:
            return {
                'username': user_obj.username
            }
        except Exception:
            return None

    def get_work_order_exec_flow(self, user_obj, instance):
        exec_flow_item_querysets = WorkOrderTaskFlowItem.objects.filter(
            belong_flow__exact=instance.order_model.order_flow_type.task_exec_flow)
        exec_flow_item_list = []
        current_exec_flow = {}
        for exec_flow_item_obj in exec_flow_item_querysets:
            exec_flow_items = {
                "id": exec_flow_item_obj.id,
                "exec_order": exec_flow_item_obj.exec_order,
                "flow_item_name": exec_flow_item_obj.flow_item_name,
                "exec_user": exec_flow_item_obj.exec_user.username
            }
            exec_flow_item_list.append(exec_flow_items)
            if user_obj is not None and exec_flow_item_obj.exec_user.id == user_obj.id:
                current_exec_flow.update(current_exec_flow=exec_flow_items)
        return exec_flow_item_list, current_exec_flow

    def get_work_order_audit_flow(self, user_obj, instance):
        audit_flow_item_querysets = WorkOrderTaskFlowItem.objects.filter(
            belong_flow__exact=instance.order_model.order_flow_type.task_audit_flow)
        audit_flow_item_list = []
        current_audit_flow = {}
        for audit_flow_item_obj in audit_flow_item_querysets:
            audit_flow_items = {
                "id": audit_flow_item_obj.id,
                "exec_order": audit_flow_item_obj.exec_order,
                "flow_item_name": audit_flow_item_obj.flow_item_name,
                "exec_user": audit_flow_item_obj.exec_user.username
            }
            audit_flow_item_list.append(audit_flow_items)
            if user_obj is not None and audit_flow_item_obj.exec_user.id == user_obj.id:
                current_audit_flow.update(current_audit_flow=audit_flow_items)
        return audit_flow_item_list, current_audit_flow

    def get_work_order_opetaion_info(self,instance):
        work_order_opration_record_queryset = WorkOrderOperation.objects.filter(
            Q(work_order__exact=instance) & ~Q(ops_status__exact=15)).order_by("create_time")
        work_order_opration_reply_queryset = WorkOrderOperation.objects.filter(
            Q(work_order__exact=instance) & Q(ops_status__exact=15)).order_by("create_time")

        operation_records = []
        for q in work_order_opration_record_queryset:
            operation_record = {
                "ops_user": q.ops_user.username,
                "ops_status": q.get_ops_status_display(),
                "create_time": q.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            operation_records.append(operation_record)
        operation_replys = []
        for q in work_order_opration_reply_queryset:
            operation_reply = {
                "ops_user": q.ops_user.username,
                "ops_status": q.get_ops_status_display(),
                "ops_reply_content": q.ops_reply_content,
                "create_time": q.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            operation_replys.append(operation_reply)

        return operation_records, operation_replys

    def to_representation(self, instance):
        ret = super(WorkOrderTaskSerializer, self).to_representation(instance)
        ret['order_model'] = instance.order_model.model_name
        ret['order_status'] = instance.get_order_status_display()
        ret['current_exec_user'] = self.get_user_info(instance.current_exec_user)
        ret['current_audit_user'] = self.get_user_info(instance.current_audit_user)
        ret['exec_flow'], ret['current_exec_flow'] = self.get_work_order_exec_flow(instance.current_exec_user, instance)
        ret['audit_flow'], ret['current_audit_flow'] = self.get_work_order_audit_flow(instance.current_audit_user,
                                                                                      instance)
        ret['operation_records'], ret['operation_replys'] = self.get_work_order_opetaion_info(instance)
        return ret

    class Meta:
        model = WorkOrderTask
        fields = "__all__"


class WorkOrderOperationSerializer(serializers.ModelSerializer):

    '''
        工单操作序列化类
    '''

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="创建日期",
                                            read_only=True,
                                            help_text="创建日期")

    ops_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def to_representation(self, instance):
        ret = super(WorkOrderOperationSerializer,self).to_representation(instance)
        ret['work_order'] = instance.work_order.order_title
        ret['ops_status'] = instance.get_ops_status_display()
        return ret

    class Meta:
        model = WorkOrderOperation
        fields = "__all__"