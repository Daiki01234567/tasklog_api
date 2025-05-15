from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import User
from .serializers import UserSerializer
from core.permissions import BaseRolePermission

class UserCreateAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [BaseRolePermission]

class UserRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [BaseRolePermission]
