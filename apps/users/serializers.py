from rest_framework import serializers

from .models import UserProfile, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    role = serializers.PrimaryKeyRelatedField(many=False, queryset=Role.objects.all(),
                                              error_messages={"does_not_exist": "role不存在"})

    def to_representation(self, instance):
        role_obj = instance.role
        ret = super(UserSerializer, self).to_representation(instance)
        ret["role"] = {
            "id": role_obj.id,
            "name": role_obj.name,
            "menulist": role_obj.menulist
        }
        return ret

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username']