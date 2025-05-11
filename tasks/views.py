from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskRoleBasedPermission
from core.services.import_service import ImportMixin

class TaskViewSet(ImportMixin, ModelViewSet):
    queryset = Task.objects.select_related('project', 'assignee').all()
    serializer_class = TaskSerializer
    model_serializer_class = TaskSerializer
    permission_classes = [IsTaskRoleBasedPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'assignee__email', 'project__name']
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status == Task.Status.DONE:
            return Response({'detail': '完了済みタスクは削除できません'}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
