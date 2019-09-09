from django.db import models
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class WorkOrderStatusCode(models.Model):

    status_code = models.IntegerField('状态码', help_text='状态码', null=False)
    status_name = models.CharField('状态名称', max_length=40, help_text='状态名称', null=False)
    status_belong_table = models.CharField('所在表格', max_length=40, help_text='所在表格', null=False)

    def __str__(self):
        return "{}: [{}]".format(self.status_name, self.status_code)

    class Meta:
        ordering = ['id']
        db_table = 'work_order_status_code'


class TemplateWorkOrderProject(models.Model):

    project_name = models.CharField('项目名称', max_length=200, help_text='项目名称')
    project_info = models.CharField('项目信息', max_length=255, help_text='项目信息')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text='创建时间')

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ['id']
        db_table = 'template_work_order_project'


class TemplateWorkOrderTaskFlow(models.Model):
    '''
        工单执行流程
    '''
    FLOW_TYPE_CHOICE = (
        (0, 'executer'),
        (1, 'audit')
    )

    flow_name = models.CharField('流程名称', max_length=200, db_index=True, unique=True,  help_text='流程名称')
    flow_type = models.IntegerField('流程类型', choices=FLOW_TYPE_CHOICE, help_text='流程类型')
    create_time = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')
    change_time = models.DateTimeField('上次修改时间', auto_now_add=True, help_text='上次修改时间')

    def __str__(self):
        return self.flow_name

    class Meta:
        ordering = ['id']
        db_table = 'template_work_order_flow'


class TemplateWorkOrderTaskFlowItem(models.Model):
    '''
        工单执行流程项
    '''

    OPS_STATUS_CHOICE = (
        (1, '提交'),
        (2, '审核通过'),
        (3, '审核不通过'),
        (4, '审核转发'),
        (5, '确认执行'),
        (6, '执行确认不通过'),
        (7, '延期执行'),
        (8, '执行完成'),
        (9, '执行转发'),
        (10, '用户确认不通过'),
        (11, '关闭'),
        (12, '重走流程'),
        (13, '重新编辑'),
        (14, '撤回工单'),
        (15, '回复'),
    )

    belong_flow = models.ForeignKey(TemplateWorkOrderTaskFlow,
                                  on_delete=models.CASCADE,
                                  help_text='所属流程名称',
                                  null=False,
                                  verbose_name='所属流程名称',
                                  related_name='belong_flow')
    flow_item_name = models.CharField('流程项名称', max_length=200, help_text='流程项名称')
    # 数字由小到大 顺序执行
    exec_order = models.IntegerField('执行顺序', help_text='执行顺序')
    exec_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  help_text='执行/审核用户',
                                  verbose_name='执行/审核用户',
                                  related_name='template_exec_user')
    ops_status = models.IntegerField('状态', choices=OPS_STATUS_CHOICE, null=True, help_text='状态')


    def __str__(self):
        return "{}[{}]".format(self.belong_flow, self.flow_item_name)

    class Meta:
        ordering = ['id']
        db_table = 'template_work_order_flow_item'


class TemplateWorkOrderFlowType(models.Model):
    '''
        工单类型表
    '''

    FLOW_TYPE_STATUS_CHOICE = (
        (0, '禁用'),
        (1, '启用')
    )

    flow_type_name = models.CharField('类型名称', max_length=200, help_text='类型名称')
    task_exec_flow = models.ForeignKey(TemplateWorkOrderTaskFlow,
                                       on_delete=models.CASCADE,
                                       help_text='工单执行流程',
                                       null=False,
                                       verbose_name='工单执行流程',
                                       related_name='task_exec_flow')
    task_audit_flow = models.ForeignKey(TemplateWorkOrderTaskFlow,
                                        on_delete=models.CASCADE,
                                        help_text='工单审核流程',
                                        null=False,
                                        verbose_name='工单审核流程',
                                        related_name='task_audit_flow')
    flow_type_status = models.IntegerField('工单状态', choices=FLOW_TYPE_STATUS_CHOICE, default=1, help_text='状态')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text="添加时间")
    change_time = models.DateTimeField('修改时间', auto_now=True,  help_text="修改时间")


    def __str__(self):
        return "{}".format(self.flow_type_name)

    class Meta:
        ordering = ['id']
        db_table = 'template_work_order_flow_type'


class TemplateWorkOrderType(models.Model):

    WORK_ORDER_TYPE_STATUS_CHOICE = (
        (0, '禁用'),
        (1, '启用')
    )

    type_name = models.CharField('类型名称', max_length=200, help_text='类型名称', db_index=True, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text="添加时间")
    change_time = models.DateTimeField('修改时间', auto_now=True, help_text="修改时间")
    type_status = models.IntegerField('是否启用', choices=WORK_ORDER_TYPE_STATUS_CHOICE, default=1, help_text='是否启用')
    link_project = models.ForeignKey(TemplateWorkOrderProject,
                                     on_delete=models.CASCADE,
                                     help_text='关联项目',
                                     null=True,
                                     verbose_name='关联项目',
                                     related_name='link_project')

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['id']
        db_table = 'template_work_order_type'


class TemplateWorkOrderModel(models.Model):
    """
        工单模板
    """
    model_name = models.CharField('模板名称', max_length=200, help_text='模板名称', db_index=True, unique=True)
    order_type = models.ForeignKey(TemplateWorkOrderType,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   help_text='工单类型',
                                   verbose_name='工单类型',
                                   related_name='order_type')
    order_flow_type = models.ForeignKey(TemplateWorkOrderFlowType,
                                        on_delete=models.CASCADE,
                                        null=False,
                                        help_text='工单流程类型',
                                        verbose_name='工单流程类型',
                                        related_name='order_flow_type')
    model_create_time = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['id']
        db_table = 'template_work_order_model'


## 工单实例
class WorkOrderProject(models.Model):

    project_name = models.CharField('项目名称', max_length=200, help_text='项目名称')
    project_info = models.CharField('项目信息', max_length=255, help_text='项目信息')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text='创建时间')

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = ['id']
        db_table = 'work_order_project'


class WorkOrderTaskFlow(models.Model):
    '''
        工单执行流程
    '''
    FLOW_TYPE_CHOICE = (
        (0, 'executer'),
        (1, 'audit')
    )

    flow_name = models.CharField('流程名称', max_length=200, help_text='流程名称')
    flow_type = models.IntegerField('流程类型', choices=FLOW_TYPE_CHOICE, help_text='流程类型')
    create_time = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')
    change_time = models.DateTimeField('上次修改时间', auto_now_add=True, help_text='上次修改时间')

    def __str__(self):
        return self.flow_name

    class Meta:
        ordering = ['id']
        db_table = 'work_order_flow'


class WorkOrderTaskFlowItem(models.Model):
    '''
        工单执行流程项
    '''
    OPS_STATUS_CHOICE = (
        (1, '提交'),
        (2, '审核通过'),
        (3, '审核不通过'),
        (4, '审核转发'),
        (5, '确认执行'),
        (6, '执行确认不通过'),
        (7, '延期执行'),
        (8, '执行完成'),
        (9, '执行转发'),
        (10, '用户确认不通过'),
        (11, '关闭'),
        (12, '重走流程'),
        (13, '重新编辑'),
        (14, '撤回工单'),
        (15, '回复'),
    )
    #
    belong_flow = models.ForeignKey(WorkOrderTaskFlow,
                                  on_delete=models.CASCADE,
                                  help_text='所属流程名称',
                                  null=False,
                                  verbose_name='所属流程名称',
                                  related_name='belong_flow')
    flow_item_name = models.CharField('流程项名称', max_length=200, help_text='流程项名称')
    # 数字由小到大 顺序执行
    exec_order = models.IntegerField('执行顺序', help_text='执行顺序')
    exec_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  help_text='执行/审核用户',
                                  verbose_name='执行/审核用户',
                                  related_name='exec_user')
    ops_status = models.IntegerField('状态', choices=OPS_STATUS_CHOICE, null=True, help_text='状态')


    def __str__(self):
        return "{}[{}]".format(self.belong_flow, self.flow_item_name)

    class Meta:
        ordering = ['id']
        db_table = 'work_order_flow_item'


class WorkOrderFlowType(models.Model):
    '''
        工单类型表
    '''

    FLOW_TYPE_STATUS_CHOICE = (
        (0, '禁用'),
        (1, '启用')
    )

    flow_type_name = models.CharField('类型名称', max_length=200, help_text='类型名称')
    task_exec_flow = models.ForeignKey(WorkOrderTaskFlow,
                                       on_delete=models.CASCADE,
                                       help_text='工单执行流程',
                                       null=False,
                                       verbose_name='工单执行流程',
                                       related_name='exec_flow')
    task_audit_flow = models.ForeignKey(WorkOrderTaskFlow,
                                        on_delete=models.CASCADE,
                                        help_text='工单审核流程',
                                        null=False,
                                        verbose_name='工单审核流程',
                                        related_name='audit_flow')
    flow_type_status = models.IntegerField('工单状态', choices=FLOW_TYPE_STATUS_CHOICE, default=1, help_text='状态')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text="添加时间")
    change_time = models.DateTimeField('修改时间', auto_now=True,  help_text="修改时间")


    def __str__(self):
        return "{}".format(self.flow_type_name)

    class Meta:
        ordering = ['id']
        db_table = 'work_order_flow_type'


class WorkOrderType(models.Model):

    WORK_ORDER_TYPE_STATUS_CHOICE = (
        (0, '禁用'),
        (1, '启用')
    )

    type_name = models.CharField('类型名称', max_length=200, help_text='类型名称', db_index=True, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text="添加时间")
    change_time = models.DateTimeField('修改时间', auto_now=True, help_text="修改时间")
    type_status = models.IntegerField('是否启用', choices=WORK_ORDER_TYPE_STATUS_CHOICE, default=1, help_text='是否启用')
    link_project = models.ForeignKey(WorkOrderProject,
                                     on_delete=models.CASCADE,
                                     help_text='关联项目',
                                     null=True,
                                     verbose_name='关联项目',
                                     related_name='link_project')

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['id']
        db_table = 'work_order_type'


class WorkOrderModel(models.Model):
    """
        工单模板实例
    """
    # inherit_model_template = models.IntegerField('继承模板', help_text='继承模板')
    # 每次新建工单时，copy 一个模型实例到对应对象中， 以后操作全部在实例中完成，模板本身不动
    model_name = models.CharField('模板名称', max_length=200, help_text='模板名称')
    order_type = models.ForeignKey(WorkOrderType,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   help_text='工单类型',
                                   verbose_name='工单类型',
                                   related_name='order_type')
    order_flow_type = models.ForeignKey(WorkOrderFlowType,
                                        on_delete=models.CASCADE,
                                        null=False,
                                        help_text='工单流程类型',
                                        verbose_name='工单流程类型',
                                        related_name='order_flow_type')
    model_create_time = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['id']
        db_table = 'work_order_model'


class WorkOrderTask(models.Model):

    '''
        工单内容表
    '''
    # ORDER_STATUS_CHOICE = WorkOrderStatusCode.objects.filter(status_belong_table__exact='work_order_task').values_list(
    #     'status_code', 'status_name')

    ORDER_STATUS_CHOICE = (
        (1, '待提交'),
        (2, '审核中'),
        (3, '执行人确认中'),
        (4, '执行人执行中'),
        (5, '执行人延期执行中'),
        (6, '执行完成,用户确认中'),
        (7, '审核驳回,等待用户确认'),
        (8, '执行驳回,等待用户确认'),
        (9, '用户确认不通过,等待执行重做'),
        (10, '完成关闭'),
        (11, '驳回关闭'),
        (12, '撤销关闭'),
    )
    order_task_id = models.UUIDField('工单ID', default=uuid.uuid4(), auto_created=True, help_text='工单ID')
    order_title = models.CharField('工单标题', max_length=100, help_text='工单标题')
    template_order_model = models.ForeignKey(TemplateWorkOrderModel,
                                    on_delete=models.CASCADE,
                                    null=False,
                                    help_text='工单模板模型 ',
                                    verbose_name='工单模板模型',
                                    related_name='template_order_model')
    order_model = models.ForeignKey(WorkOrderModel,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    default=None,
                                    help_text='工单模板 实例',
                                    verbose_name='工单模板 实例',
                                    related_name='order_model')
    created_user = models.ForeignKey(User,
                                     on_delete=models.CASCADE,
                                     null=False,
                                     help_text='创建用户',
                                     verbose_name='创建用户',
                                     related_name='created_user')
    order_purpose = models.TextField('工单需求', help_text='工单需求')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField('更新时间', auto_now=True, help_text='更新时间')
    current_exec_user = models.ForeignKey(User,
                                          on_delete=models.CASCADE,
                                          null=True,
                                          help_text='当前执行用户',
                                          verbose_name='当前执行用户',
                                          related_name='current_exec_user')
    current_audit_user = models.ForeignKey(User,
                                           on_delete=models.CASCADE,
                                           null=True,
                                           help_text='当前审核用户',
                                           verbose_name='当前审核用户',
                                           related_name='current_audit_user')
    order_result = models.TextField('工单结果', default=None, null=True, help_text='工单结果')
    order_status = models.IntegerField('工单状态', choices=ORDER_STATUS_CHOICE, default=1, help_text='工单状态')

    def __str__(self):
        return "{}[{}]".format(self.order_title, self.order_task_id)

    class Meta:
        ordering = ['create_time']
        db_table = 'work_order_task'


class WorkOrderOperation(models.Model):

    '''
        工单操作表
    '''
    # OPS_STATUS_CHOICE = WorkOrderStatusCode.objects.filter(status_belong_table__exact='work_order_operation').values_list(
    #     'status_code', 'status_name')
    OPS_STATUS_CHOICE = (
        (1, '提交'),
        (2, '审核通过'),
        (3, '审核不通过'),
        (4, '审核转发'),
        (5, '确认执行'),
        (6, '执行确认不通过'),
        (7, '延期执行'),
        (8, '执行完成'),
        (9, '执行转发'),
        (10, '用户确认不通过'),
        (11, '关闭'),
        (12, '重走流程'),
        (13, '重新编辑'),
        (14, '撤回工单'),
        (15, '回复'),
    )

    work_order = models.ForeignKey(WorkOrderTask,
                                   on_delete=models.CASCADE, null=False,
                                   help_text='工单名称',
                                   verbose_name='工单名称',
                                   related_name='work_order_task')
    ops_user = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 null=False,
                                 help_text='执行用户',
                                 verbose_name='执行用户',
                                 related_name='work_order_ops_user')
    ops_status = models.IntegerField('操作状态', choices=OPS_STATUS_CHOICE, help_text='操作状态')
    ops_reply_content = models.TextField('回复内容', null=True, help_text='回复内容')
    create_time = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')


    class Meta:
        ordering = ['id']
        db_table = 'work_order_operation'