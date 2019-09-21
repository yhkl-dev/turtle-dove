from django.db import models

# Create your models here.

class Project(models.Model):

    DELETE_PROJECT_STATUS = (
        (0, '否'),
        (1, '是')
    )

    project_name_en = models.CharField('项目名称(english)', max_length=100, help_text='项目名称(english)')
    project_name_zh = models.CharField('项目名称(chinese)', max_length=100,  help_text='项目名称(chinese')
    is_deleted = models.IntegerField('是否删除', choices=DELETE_PROJECT_STATUS, default=0, help_text='是否删除')

    def __str__(self):
        return '{}[{}]'.format(self.project_name_zh, self.project_name_en)

    class Meta:
        ordering = ['id']
        db_table = 'projects'


class ProjectConfigure(models.Model):

    item_name = models.CharField('参数名称', max_length=100, help_text='参数名称')
    item_value = models.CharField('参数值', max_length=100, help_text='参数值')
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text='所属项目',
                                       null=False, verbose_name='所属项目')

    def __str__(self):
        return '{}: {}'.format(self.item_name, self.item_value)

    class Meta:
        ordering = ['id']
        db_table = 'projects_configure'


class ProjectPlatformEnv(models.Model):

    platform_name = models.CharField("平台名称", max_length=20, db_index=True, unique=True, help_text='平台名称')

    def __str__(self):
        return self.platform_name

    class Meta:
        ordering = ['id']
        db_table = 'project_platform'
