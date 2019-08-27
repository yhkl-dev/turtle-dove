from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkOrder(models.Model):

    STATUS = (
        (0, '申请'),
        (1, '处理中'),
        (2, '执行中'),
        (3, '完成'),
        (4, '失败'),
    )

    title = models.CharField(max_length=100, verbose_name='标题')
    order_content = models.TextField('内容')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_order_applicant', verbose_name='申请人')
    processor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_order_applicant', verbose_name='处理人')
    order_status = models.IntegerField(choices=STATUS)
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    complete_time = models.DateTimeField(auto_now=True, verbose_name='处理完成时间')

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = '工单'
        db_table = 'version_work_order'
        ordering = ['complete_time']
