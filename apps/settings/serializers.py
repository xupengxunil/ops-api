from rest_framework import serializers
from .models import Setting
import json


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(SettingsSerializer, self).to_representation(instance)
        ret["value"] = json.loads(ret["value"])
        return ret