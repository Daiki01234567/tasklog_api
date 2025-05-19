from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.deletion import ProtectedError

from .models import Project
from .serializers import ProjectSerializer
from core.permissions import BaseRolePermission
from core.services.import_service import ImportMixin

import logging

logger = logging.getLogger(__name__)

class ProjectViewSet(ImportMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    model_serializer_class  = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [BaseRolePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.delete()
        except ProtectedError:
            logger.exception(f"Project(id={obj.id}, name={obj.name}) の削除に失敗しました。保護された関連オブジェクトが存在します。")
            return Response({
                'ProtectedError': '関連するタスクがあるため削除できません。'
                }, status=status.HTTP_409_CONFLICT
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
