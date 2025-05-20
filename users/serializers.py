from rest_framework import serializers
from .models import User
from core.serializers.user import BaseUserSerializer

class UserSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['password']

    def create(self, validated_data):
        validated_data.pop('role', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
        