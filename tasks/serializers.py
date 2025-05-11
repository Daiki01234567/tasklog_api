from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Project, Task
from users.models import User
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField (
        queryset=Project.objects.all(),
        write_only=True
    )
    assignee = serializers.PrimaryKeyRelatedField (
        queryset=User.objects.all(),
        write_only=True
    )
    project_name = serializers.CharField(source='project.name', read_only=True)
    assignee_email = serializers.CharField(source='assignee.email', read_only=True)
    planned_hours = serializers.IntegerField(min_value=0)
    due_date=serializers.DateField(
        format='%Y-%m-%d',
        input_formats=[
            '%Y', '%Y-%m', '%Y-%m-%d', '%Y%m%d'
        ]
    )

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_name',
            'title',  'planned_hours', 
            'assignee', 'assignee_email',
            'status', 'due_date',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Task.objects.select_related('project').all(),
                fields=['project', 'title'],
                message='同じプロジェクト内でタイトルは一意でなければなりません。'
            )
        ]

    def validate_due_date(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError('due_dateは未来の日付を指定してください。')
        return value
