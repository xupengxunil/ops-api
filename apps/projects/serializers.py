from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Project, Group, Company, Role, ProjectUser
from apps.users.models import UserProfile


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    group_cn = serializers.PrimaryKeyRelatedField(many=False, queryset=Company.objects.all(),
                                                 error_messages={"does_not_exist": "不存在"})

    class Meta:
        model = Group
        fields = "__all__"

    def to_representation(self, instance):
        company_obj = instance.group_cn
        ret = super(GroupSerializer, self).to_representation(instance)
        ret["group_cn"] = {
            "id": company_obj.id,
            "company_nickname": company_obj.company_nickname,
            "company_code": company_obj.company_code
        }
        return ret


class ProjectSerializer(ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects.all(),
                                               error_messages={"does_not_exist": "不存在"})

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'project_code', 'group')

    def to_representation(self, instance):
        group_obj = instance.group
        ret = super(ProjectSerializer, self).to_representation(instance)
        ret["group"] = {
            "id": group_obj.id,
            "group_name": group_obj.group_name,
            "group_code": group_obj.group_code
        }
        return ret

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class ProjectUserSerializer(ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(many=False, queryset=UserProfile.objects.all(),error_messages={"dose_not_exist": "不存在"} )
    role = serializers.PrimaryKeyRelatedField(many=False, queryset=Role.objects.all(),error_messages={"dose_not_exist": "不存在"})

    class Meta:
        model = ProjectUser
        fields = "__all__"

    def to_representation(self, instance):
        user_obj =  instance.user
        role_obj = instance.role
        ret = super(ProjectUserSerializer,self).to_representation(instance)

        ret["user"] = {
            "id": user_obj.id,
            "name": user_obj.username
        }

        ret["role"] = {
            "id": role_obj.id,
            "role_name": role_obj.role_name
        }

        return ret