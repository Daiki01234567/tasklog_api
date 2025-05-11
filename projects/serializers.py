from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']

