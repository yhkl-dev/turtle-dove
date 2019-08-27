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

    def to_representation(self, instance):
        server_purpose = self.get_product_name(instance.server_purpose)
        service = self.get_product_name(instance.service)

        resource_type_obj = instance.resource_type
        user_obj = instance.belong_user
        ret = super(ResourceSerializer, self).to_representation(instance)
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
        resource_obj = Resource.objects.get(instance.belong_resource)
        ret = super(ResourceUserSerializer, self).to_representation(instance)
        ret["belong_resource"] = resource_obj.resource_name
        return ret

    class Meta:
        model = ResourceUser
        fields = '__all__'
