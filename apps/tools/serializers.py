from rest_framework import serializers

from apps.users.models import UserProfile
from .models import Todolist


class TodolistSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        todo = Todolist.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        return todo

    class Meta:
        model = Todolist
        fields = ['id','user','content','type','status']
