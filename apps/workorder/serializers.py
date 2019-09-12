from rest_framework import serializers
from django.db.models import Q
from .models import (WorkOrderTask,
                     WorkOrderOperation,
                     WorkOrderTaskFlowItem,
                     WorkOrderStatusCode,
                     TemplateWorkOrderProject,
                     TemplateWorkOrderFlowType,
                     TemplateWorkOrderTaskFlow,
                     TemplateWorkOrderTaskFlowItem,
                     TemplateWorkOrderType,
                     TemplateWorkOrderModel,
                     WorkOrderModel,
                     WorkOrderTaskFlow,
                     WorkOrderType,
                     WorkOrderFlowType)


class WorkOrderStatusCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkOrderStatusCode
        fields = ['status_code', 'status_name']


class TemplateWorkOrderTaskFlowItemSerializer(serializers.ModelSerializer):
    '''
        工单执行流程项 模板 序列化类
    '''

    def to_representation(self, instance):
        ret = super(TemplateWorkOrderTaskFlowItemSerializer, self).to_representation(instance)
        ret['belong_flow'] = instance.belong_flow.flow_name
        ret['exec_user'] = instance.exec_user.username
        return ret

    # def validate(self, attrs):
    #     task_flow_queryset = TemplateWorkOrderTaskFlowItem.objects.filter(
    #         Q(belong_flow__exact=attrs.get("belong_flow")) & ~Q(exec_user=attrs.get('exec_user'))).values('exec_order')
    #     c = [q.get('exec_order') for q in task_flow_queryset]
    #     users = [q.get('exec_user') for q in task_flow_queryset]
    #
    #     if attrs.get("exec_order") in c:
    #         raise serializers.ValidationError('Duplicated exec_order')
    #     elif attrs.get("exec_user") in users:
    #         raise serializers.ValidationError('Duplicated exec_user')
    #     else:
    #         return attrs


    class Meta:
        model = TemplateWorkOrderTaskFlowItem
        fields = "__all__"


class TemplateWorkOrderTaskFlowSerializer(serializers.ModelSerializer):

    '''
        工单执行流程 模板 序列化类
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
        task_flow_item_queryset = TemplateWorkOrderTaskFlowItem.objects.filter(belong_flow__exact=instance).order_by('exec_order')
        flow_item_sets = []
        for q in task_flow_item_queryset:
            flow_item = {
                "id": q.id,
                "exec_order": q.exec_order,
                "flow_item_name": q.flow_item_name,
                "exec_user": q.exec_user.username
            }
            flow_item_sets.append(flow_item)
        ret = super(TemplateWorkOrderTaskFlowSerializer, self).to_representation(instance)
        ret['flow_type'] = instance.get_flow_type_display()
        ret['flow_item'] = flow_item_sets
        return ret

    class Meta:
        model = TemplateWorkOrderTaskFlow
        fields = '__all__'


class TemplateWorkOrderFlowTypeSerializer(serializers.ModelSerializer):

    '''
        工单执行流程类型 模板 序列化类
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
        ret = super(TemplateWorkOrderFlowTypeSerializer, self).to_representation(instance)
        # ret['flow_type_status'] = instance.get_flow_type_status_display()
        ret['flow_type_status_name'] = instance.get_flow_type_status_display()
        ret['task_exec_flow_name'] = instance.task_exec_flow.flow_name
        ret['task_audit_flow_name'] = instance.task_audit_flow.flow_name
        return ret


    class Meta:
        model = TemplateWorkOrderFlowType
        fields = "__all__"


class TemplateWorkOrderTypeSerializer(serializers.ModelSerializer):

    '''
        工单类型 模板 序列化类
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
        ret = super(TemplateWorkOrderTypeSerializer, self).to_representation(instance)
        # ret['type_status'] = instance.get_type_status_display()
        ret['type_status_name'] = instance.get_type_status_display()
        return ret

    class Meta:
        model = TemplateWorkOrderType
        fields = "__all__"


class TemplateWorkOrderProjectSerializer(serializers.ModelSerializer):

    '''
        工单项目序列化类
    '''
    class Meta:
        model = TemplateWorkOrderProject
        fields = "__all__"


class TemplateWorkOrderModelSerializer(serializers.ModelSerializer):

    '''
        工单模板序列化类
    '''

    model_create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                                  label="创建日期",
                                                  read_only=True,
                                                  help_text="创建日期")

    def get_order_type(self, order_type_obj):
        try:
            return {
                "id": order_type_obj.id,
                "type_name": order_type_obj.type_name,
                # "type_status": order_type_obj.type_status,
                "type_status_name": order_type_obj.get_type_status_display(),
                "create_time": order_type_obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        except Exception:
            return {}

    def get_order_flow_type(self, order_flow_type_obj):
        try:
            return {
                "flow_type_id": order_flow_type_obj.id,
                "flow_type_name": order_flow_type_obj.flow_type_name,
                # "flow_type_status": order_flow_type_obj.flow_type_status,
                "flow_type_status_name": order_flow_type_obj.get_flow_type_status_display(),
                "task_exec_flow": self.get_task_flow(order_flow_type_obj.task_exec_flow),
                "task_exec_flow_items": self.get_flow_items(order_flow_type_obj.task_exec_flow),
                "task_audit_flow": self.get_task_flow(order_flow_type_obj.task_audit_flow),
                "task_audit_flow_items": self.get_flow_items(order_flow_type_obj.task_audit_flow)
            }
        except Exception as e:
            return {}

    def get_flow_items(self, order_flow_type_obj):
        item_queryset = TemplateWorkOrderTaskFlowItem.objects.filter(belong_flow__exact=order_flow_type_obj).order_by(
            'exec_order')
        item_list = []
        for item_obj in item_queryset:
            item = {
                "flow_item_name": item_obj.flow_item_name,
                "exec_order": item_obj.exec_order,
                "exec_user": item_obj.exec_user.username
            }
            item_list.append(item)
        return item_list

    def get_task_flow(self, task_flow_obj):
        try:
            return {
                "flow_name": task_flow_obj.flow_name,
                "flow_type": task_flow_obj.flow_type,
                "create_time": task_flow_obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return {}

    def to_representation(self, instance):
        ret = super(TemplateWorkOrderModelSerializer,self).to_representation(instance)
        ret['order_type_name'] = instance.order_type.type_name
        ret['order_flow_type_name'] = instance.order_flow_type.flow_type_name
        return ret


    class Meta:
        model = TemplateWorkOrderModel
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

    order_model = serializers.HiddenField(default=None)

    def get_user_info(self, user_obj):
        try:
            return  user_obj.username
        except Exception:
            return None

    def get_work_order_exec_flow(self, user_obj, instance):
        exec_flow_item_queryset = WorkOrderTaskFlowItem.objects.filter(
            belong_flow__exact=instance.order_model.order_flow_type.task_exec_flow)
        exec_flow_item_list = []
        current_exec_flow = {}
        for exec_flow_item_obj in exec_flow_item_queryset:
            exec_flow_items = {
                "id": exec_flow_item_obj.id,
                "exec_order": exec_flow_item_obj.exec_order,
                "flow_item_name": exec_flow_item_obj.flow_item_name,
                "exec_user": exec_flow_item_obj.exec_user.username,
                "status_code": exec_flow_item_obj.ops_status,
                "status_name": exec_flow_item_obj.get_ops_status_display(),
            }
            exec_flow_item_list.append(exec_flow_items)
            if user_obj is not None and exec_flow_item_obj.exec_user == user_obj:
                current_exec_flow = exec_flow_items.copy()
        return exec_flow_item_list, current_exec_flow

    def get_work_order_audit_flow(self, user_obj, instance):
        audit_flow_item_queryset = WorkOrderTaskFlowItem.objects.filter(
            belong_flow__exact=instance.order_model.order_flow_type.task_audit_flow)
        audit_flow_item_list = []
        current_audit_flow = None
        for audit_flow_item_obj in audit_flow_item_queryset:
            audit_flow_items = {
                "id": audit_flow_item_obj.id,
                "exec_order": audit_flow_item_obj.exec_order,
                "flow_item_name": audit_flow_item_obj.flow_item_name,
                "exec_user": audit_flow_item_obj.exec_user.username,
                "status_code": audit_flow_item_obj.ops_status,
                "status_name": audit_flow_item_obj.get_ops_status_display(),
            }
            audit_flow_item_list.append(audit_flow_items)
            if user_obj is not None and audit_flow_item_obj.exec_user == user_obj:
                current_audit_flow = audit_flow_items.copy()
        return audit_flow_item_list, current_audit_flow

    def get_work_order_opetaion_info(self,instance):
        work_order_operation_record_queryset = WorkOrderOperation.objects.filter(
            Q(work_order__exact=instance) & ~Q(ops_status__exact=15)).order_by("create_time")
        work_order_operation_reply_queryset = WorkOrderOperation.objects.filter(
            Q(work_order__exact=instance) & Q(ops_status__exact=15)).order_by("create_time")

        operation_records = []
        for q in work_order_operation_record_queryset:
            operation_record = {
                "ops_user": q.ops_user.username,
                "status_code": q.ops_status,
                "status_name": q.get_ops_status_display(),
                "ops_reply_content": q.ops_reply_content,
                "create_time": q.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            operation_records.append(operation_record)
        operation_replys = []
        for q in work_order_operation_reply_queryset:
            operation_reply = {
                "ops_user": q.ops_user.username,
                "status_code": q.ops_status,
                "status_name": q.get_ops_status_display(),
                "ops_reply_content": q.ops_reply_content,
                "create_time": q.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            operation_replys.append(operation_reply)

        return operation_records, operation_replys

    def to_representation(self, instance):
        ret = super(WorkOrderTaskSerializer, self).to_representation(instance)
        ret.pop('order_status')
        ret['order_model'] = instance.order_model.model_name
        ret['status_code'] = instance.order_status
        ret['status_name'] = instance.get_order_status_display()
        ret['current_exec_user'] = self.get_user_info(instance.current_exec_user)
        ret['current_audit_user'] = self.get_user_info(instance.current_audit_user)
        ret['exec_flow'], ret['current_exec_flow'] = self.get_work_order_exec_flow(instance.current_exec_user, instance)
        ret['audit_flow'], ret['current_audit_flow'] = self.get_work_order_audit_flow(instance.current_audit_user,
                                                                                      instance)
        ret['operation_records'], ret['operation_logs'] = self.get_work_order_opetaion_info(instance)
        return ret

    def copy_field(self, origin_model, target_model):
        for field in origin_model._meta.fields:
            setattr(target_model, field.name, getattr(origin_model, field.name))
        return target_model

    def _create_order_model_instance(self, order_model_template):
        order_model_obj = WorkOrderModel()
        order_model_obj.model_name = order_model_template.model_name
        # 处理 order type
        template_work_order_type_obj = order_model_template.order_type
        work_order_type_obj = WorkOrderType()
        work_order_type_obj = self.copy_field(template_work_order_type_obj, work_order_type_obj)
        work_order_type_obj.save()

        # 处理 work order flow type
        template_work_order_flow_type_obj = order_model_template.order_flow_type

        template_work_order_flow_exec_obj = template_work_order_flow_type_obj.task_exec_flow
        work_order_flow_exec_obj = WorkOrderTaskFlow()
        # work_order_flow_exec_obj = self.copy_field(template_work_order_flow_exec_obj, work_order_flow_exec_obj)
        work_order_flow_exec_obj.flow_name = template_work_order_flow_exec_obj.flow_name
        work_order_flow_exec_obj.flow_type = template_work_order_flow_exec_obj.flow_type
        work_order_flow_exec_obj.save()

        template_work_order_flow_audit_obj = template_work_order_flow_type_obj.task_audit_flow
        work_order_flow_audit_obj = WorkOrderTaskFlow()
        # work_order_flow_audit_obj = self.copy_field(template_work_order_flow_audit_obj, work_order_flow_audit_obj)
        work_order_flow_audit_obj.flow_name = template_work_order_flow_audit_obj.flow_name
        work_order_flow_audit_obj.flow_type = template_work_order_flow_audit_obj.flow_type
        work_order_flow_audit_obj.save()

        work_order_flow_type_obj = WorkOrderFlowType()
        # work_order_flow_type_obj = self.copy_field(template_work_order_flow_type_obj, work_order_flow_type_obj)
        work_order_flow_type_obj.flow_type_name = template_work_order_flow_type_obj.flow_type_name
        work_order_flow_type_obj.flow_type_status = template_work_order_flow_type_obj.flow_type_status
        # work_order_flow_type_obj.pk = None

        work_order_flow_type_obj.task_exec_flow = work_order_flow_exec_obj
        work_order_flow_type_obj.task_audit_flow = work_order_flow_audit_obj
        ## order_flow_type

        work_order_flow_type_obj.save()

        order_model_obj.order_flow_type = work_order_flow_type_obj
        order_model_obj.order_type = work_order_type_obj


        # 处理工单流程项
        template_work_order_flow_exec_item_queryset = TemplateWorkOrderTaskFlowItem.objects.filter(
            belong_flow=template_work_order_flow_exec_obj)

        template_work_order_flow_audit_item_queryset = TemplateWorkOrderTaskFlowItem.objects.filter(
            belong_flow=template_work_order_flow_audit_obj)

        for q in template_work_order_flow_exec_item_queryset:
            work_order_flow_item_obj = WorkOrderTaskFlowItem()
            work_order_flow_item_obj.flow_item_name = q.flow_item_name
            work_order_flow_item_obj.exec_order = q.exec_order
            work_order_flow_item_obj.exec_user = q.exec_user
            work_order_flow_item_obj.ops_status = q.ops_status
            work_order_flow_item_obj.belong_flow = work_order_flow_exec_obj
            work_order_flow_item_obj.save()

        for q in template_work_order_flow_audit_item_queryset:
            work_order_flow_item_obj = WorkOrderTaskFlowItem()
            work_order_flow_item_obj.flow_item_name = q.flow_item_name
            work_order_flow_item_obj.exec_order = q.exec_order
            work_order_flow_item_obj.exec_user = q.exec_user
            work_order_flow_item_obj.ops_status = q.ops_status
            work_order_flow_item_obj.belong_flow = work_order_flow_audit_obj
            work_order_flow_item_obj.save()


        order_model_obj.save()
        return order_model_obj

    def create(self, validated_data):
        validated_data['order_model'] = self._create_order_model_instance(validated_data['template_order_model'])
        instance = self.Meta.model.objects.create(**validated_data)
        return instance

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