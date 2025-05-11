from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Task, WorkLog
from users.models import User
from django.utils import timezone

class WorkLogSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField (
        queryset=Task.objects.select_related('project', 'assignee').all(),
        write_only=True
    )
    user = serializers.PrimaryKeyRelatedField (
        queryset=User.objects.all(),
        write_only=True
    )
    spent_hours = serializers.IntegerField(min_value=0)
    work_date = serializers.DateField(
        format='%Y-%m-%d',
        input_formats=['%Y-%m-%d', '%Y%m%d']
    )
    
    title = serializers.CharField(source='task.title', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = WorkLog
        fields = [
            'id', 'task', 'title',
            'user', 'email',
            'spent_hours','work_date'
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=WorkLog.objects.select_related('task__project', 'user').all(),
                fields=['task', 'work_date'],
                message='同じタスク内のwork_dateは一意でなければなりません。'
            )
        ]

    def validate_work_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError('work_dateは過去の日付を指定してください。')
        return value
