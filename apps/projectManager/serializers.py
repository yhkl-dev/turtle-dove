from .models import Project, ProjectConfigure
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):


    def to_representation(self, instance):
        configure_queryset = ProjectConfigure.objects.filter(belong_project=instance)
        configurations = []
        for q in configure_queryset:
            data = {
                "id": q.id,
                "name": q.item_name,
                "value": q.item_value
            }
            configurations.append(data)
        ret = super(ProjectSerializer, self).to_representation(instance)
        ret['project_name'] = "{}[{}]".format(instance.project_name_zh, instance.project_name_en)
        ret['configurations'] = configurations
        ret.pop('project_name_zh')
        ret.pop('is_deleted')
        ret.pop('project_name_en')
        return ret


    class Meta:
        model = Project
        fields = '__all__'


class ProjectConfigureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectConfigure
        fields = '__all__'