from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class ResourceType(models.Model):

    type_name = models.CharField('资源类型名称', max_length=30, default=None, help_text='资源类型名称')
    type_icon = models.CharField('资源图标', max_length=20, default=None, help_text='资源图标')

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['id']
        db_table = 'resource_type'


class Resource(models.Model):

    resource_name = models.CharField('资源名称', max_length=200, default=None, db_index=True, unique=True, help_text='资源名称')
    manage_ip = models.GenericIPAddressField('管理IP', default=None, db_index=True, help_text="管理IP")
    inner_ip = models.GenericIPAddressField('内网IP', default=None, help_text="内网IP")
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, null=True, verbose_name='资源类型',
                                      related_name="resource_type", help_text='资源类型')
    belong_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='添加用户')
    service = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name="一级业务线",
                                related_name="service", help_text="一级业务线")
    server_purpose = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name="二级产品线",
                                       related_name="server_purpose", help_text="二级产品线")
    add_time = models.DateTimeField("添加时间", auto_now=True, help_text="添加时间")
    description = models.CharField('描述', max_length=200, default=None, blank=True, help_text='描述')

    def __str__(self):
        return "{}".format(self.resource_name)

    class Meta:
        ordering = ['id']
        db_table = 'resource'


class ResourceUser(models.Model):

    IS_SUPERUSER = (
        (0, '是'),
        (1, '否')
    )

    user_name = models.CharField('用户名称', max_length=30, default=None, help_text='用户名称')
    user_password = models.CharField('用户名称', max_length=255, default=None, help_text='用户密码')
    port = models.IntegerField('端口', default=22, help_text='端口')
    private_key = models.FileField(upload_to='private_keys/', max_length=200, default=None, blank=True, null=True,
                                   verbose_name='private keys')
    create_time = models.DateTimeField('创建日期', auto_now=True, help_text='创建日期')
    last_login_time = models.DateTimeField("上次登录时间", null=True, default=None, help_text="上次登录时间")
    belong_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, help_text='所属资源',
                                        verbose_name='所属资源', related_name='resource')
    is_superuser = models.IntegerField('是否为root账户', default=0, choices=IS_SUPERUSER, help_text='是否为root账户')

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['id']
        db_table = 'resource_users'
