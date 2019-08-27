from rest_framework import serializers
from .models import Tasks, AdHocTasks
import os
import json


class TasksSerializer(serializers.ModelSerializer):
    """
    任务序列化类
    """
    add_time  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="任务创建时间")
    exec_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, help_text="任务执行时间")
    # result_view = serializers.CharField(max_length=500, required=False, help_text='执行结果')

    class Meta:
        model = Tasks
        fields = "__all__"

    def to_representation(self, instance):
        playbook = instance.playbook
        ret = super(TasksSerializer, self).to_representation(instance)
        ret['playbook'] = os.path.basename(playbook.path)
        return ret

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance

class AdHocTasksSerializer(serializers.ModelSerializer):
    """
    任务序列化类
    """
    add_time  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="任务创建时间")
    exec_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, help_text="任务执行时间")
    # result_view = serializers.CharField(max_length=500, required=False, help_text='执行结果')

    class Meta:
        model = AdHocTasks
        fields = "__all__"

    # def to_representation(self, instance):
    #     playbook = instance.playbook
    #     ret = super(AdHocTasksSerializer, self).to_representation(instance)
    #     ret['playbook'] = os.path.basename(playbook.path)
    #     return ret

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance
