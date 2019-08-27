from rest_framework import serializers
from .models import Opsdocs


class OpsDocsSerialziers(serializers.ModelSerializer):
    belong_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建日期", read_only=True, help_text="创建日期")

    def to_representation(self, instance):
        ret = super(OpsDocsSerialziers, self).to_representation(instance)
        ret['belong_user'] = instance.belong_user.username

        return ret

    class Meta:
        model = Opsdocs
        fields = "__all__"