from rest_framework import serializers
from core.serializers.user import BaseUserSerializer

class UserSerializer(BaseUserSerializer):
    role = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['password']
