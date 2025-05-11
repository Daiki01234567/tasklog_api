from rest_framework.permissions import BasePermission 
from users.models import User

import logging

class BaseRolePermission(BasePermission):
    logger = logging.getLogger(__name__)
    role_actions = {
        User.Role.PM:  ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'],
        User.Role.DEV: ['list', 'retrieve'],
        User.Role.ACC: []
    }
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role == User.Role.PM:
            return True
        
        allowed = self.role_actions.get(request.user.role, [])
        if not allowed:
            self.logger.warning(f"Undefined role: {request.user.role}")
        return view.action in allowed