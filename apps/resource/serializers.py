from rest_framework import serializers
from .models import Host, HostUser, Config
from apps.projects.models import Project

class HostUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostUser
        fields = ['id','username','password']



class HostSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=Project.objects.all(),
                                                 error_messages={"does_not_exist": "Project不存在"})

    users = HostUserSerializer(many=True,read_only=True)

    class Meta:
        model = Host
        fields = ['id', 'env', 'hostname', 'ip_address', 'operating_system', 'cpu_cores', 'memory_size', 'disk_space',
                  'description', 'status', 'project','monitor_port','users','app']

    def to_representation(self, instance):
        project_obj = instance.project
        ret = super(HostSerializer, self).to_representation(instance)
        ret["project"] = {
            "id": project_obj.id,
            "project_name": project_obj.project_name,
            "project_code": project_obj.project_code,
        }
        return ret

class ConfigSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=Project.objects.all(),
                                                 error_messages={"does_not_exist": "Project不存在"})
    class Meta:
        model = Config
        fields = "__all__"

    def to_representation(self, instance):
        project_obj = instance.project
        ret = super(ConfigSerializer, self).to_representation(instance)
        ret["project"] = {
            "id": project_obj.id,
            "project_name": project_obj.project_name,
            "project_code": project_obj.project_code,
        }
        return ret

