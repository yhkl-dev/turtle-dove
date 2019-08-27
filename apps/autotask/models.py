from django.db import models


class Tasks(models.Model):
    STATUS_CHOICE = (
        ('Y', '已执行'),
        ('R', '执行中'),
        ('N', '未执行')
    )
    VISIBLE_CHOICE = (
        ('Y', '可见'),
        ('N', '不可见'),
    )
    name = models.CharField(max_length=128, verbose_name='任务名称')
    playbook = models.FileField(upload_to='playbook/%Y/%m', max_length=200, verbose_name='playbook文件')
    detail_result = models.TextField(verbose_name='执行结果详情',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='N', verbose_name='执行状态')
    result_view = models.CharField(max_length=500, null=True, verbose_name='执行结果')
    is_visible = models.CharField(max_length=2, choices=VISIBLE_CHOICE, default='Y', verbose_name='是否可见')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')
    exec_time = models.DateTimeField(auto_now=True, verbose_name='执行时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'playbook_tasks'
        verbose_name = '任务'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

class AdHocTasks(models.Model):
    STATUS_CHOICE = (
        ('Y', '已执行'),
        ('R', '执行中'),
        ('N', '未执行')
    )
    VISIBLE_CHOICE = (
        ('Y', '可见'),
        ('N', '不可见'),
    )
    USED_MODEL = (
        ('copy','copy'),
        ('ping', 'ping'),
        ('cron','cron'),
        ('service', 'service'),
        ('shell','shell'),
        ('script','script'),
        ('yum','yum'),
        ('setup','setup'),
        ('file','file'),
        ('group','group'),
        ('user', 'user'),
        ('stat', 'stat'),
        ('mount','mount')
    )
    name = models.CharField(max_length=128, verbose_name='任务名称')
    exec_host = models.CharField(max_length=200, null=True, verbose_name='执行主机ip')
    model_name =models.CharField(max_length=30, choices=USED_MODEL, null=True,  verbose_name='模块名称')
    model_args = models.CharField(max_length=100, null=True, verbose_name='模块参数')
    detail_result = models.TextField(verbose_name='执行结果详情',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='N', verbose_name='执行状态')
    result_view = models.CharField(max_length=500, null=True, verbose_name='执行结果')
    is_visible = models.CharField(max_length=2, choices=VISIBLE_CHOICE, default='Y', verbose_name='是否可见')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')
    exec_time = models.DateTimeField(auto_now=True, verbose_name='执行时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ad_hoc_tasks'
        verbose_name = 'Ad-hoc任务'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
