from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Resource, ResourceType, ResourceUser

User = get_user_model()


class ResourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResourceType
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):

    belong_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建日期", read_only=True, help_text="创建日期")

    def get_product_name(self, product_obj):
        try:
            return {
                "name": product_obj.service_name,
                "id": product_obj.id
            }
        except Exception:
            return {}

    def get_resource_user_info(self, resource_user_obj):
        try:
            return {
                "create_time": resource_user_obj.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "last_login_time":
                    resource_user_obj.last_login_time if resource_user_obj.last_login_time is None else resource_user_obj.last_login_time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_name": resource_user_obj.user_name,
                "user_password": resource_user_obj.user_password,
                "port": resource_user_obj.port,
                # "private_key": resource_user_obj.private_key,
                "is_superuser": resource_user_obj.get_is_superuser_display()
            }
        except Exception as e:
            print(e)
            return {}

    def to_representation(self, instance):
        server_purpose = self.get_product_name(instance.server_purpose)
        service = self.get_product_name(instance.service)
        resource_user_queryset = ResourceUser.objects.filter(belong_resource__exact=instance)
        resource_type_obj = instance.resource_type
        user_obj = instance.belong_user
        ret = super(ResourceSerializer, self).to_representation(instance)
        ret["resource_user_info"] = []
        for resource_user_obj in resource_user_queryset:
            ret["resource_user_info"].append(self.get_resource_user_info(resource_user_obj))
        ret["server_purpose"] = server_purpose
        ret["service"] = service
        ret['type_name'] = resource_type_obj.type_name
        ret['type_icon'] = resource_type_obj.type_icon
        ret['belong_user'] = user_obj.username
        return ret

    class Meta:
        model = Resource
        fields = '__all__'


class ResourceUserSerializer(serializers.ModelSerializer):

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建日期", read_only=True, help_text="创建日期")
    last_login_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="上次登录日期", required=False, help_text="上次登录日期")

    def to_representation(self, instance):

        resource_obj = Resource.objects.get(id=instance.belong_resource.id)
        ret = super(ResourceUserSerializer, self).to_representation(instance)
        ret["belong_resource"] = resource_obj.resource_name
        return ret

    class Meta:
        model = ResourceUser
        fields = '__all__'

