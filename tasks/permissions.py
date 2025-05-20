from users.models import User
from core.permissions import BaseRolePermission

class IsTaskRolePermission(BaseRolePermission):
    role_actions = {
        User.Role.DEV: ['list', 'retrieve', 'partial_update', 'create'],
        User.Role.ACC: ['list', 'retrieve'],
    }

    def has_object_permission(self, request, view, obj):
        allowed = self.role_actions.get(request.user.role, [])
        if not allowed:
            self.logger.warning(f"Undefined role: {request.user.role}")
        
        if request.user.role == User.Role.PM:
            return True
        if request.user.role == User.Role.DEV:
            return obj.assignee == request.user and view.action in allowed
        
        return False
