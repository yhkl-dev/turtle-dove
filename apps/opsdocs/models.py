from django.db import models
# from tinymce.models import HTMLField
from django.contrib.auth import get_user_model

User = get_user_model()


class Opsdocs(models.Model):

    doc_name = models.CharField("文件名称", max_length=200, default=None, help_text="文件名称")
    add_time = models.DateTimeField("添加时间", auto_now=True, help_text="添加时间")
    doc_type = models.CharField("tag", max_length=200, default=None, help_text="tag")
    doc_content = models.TextField("文档内容")
    description = models.CharField('摘要', max_length=200, default=None, help_text='摘要')
    belong_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='添加用户')

    def __str__(self):
        return self.doc_name

    class Meta:
        ordering = ['id']
        db_table = 'ops_docs'
