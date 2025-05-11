from users.models import User
from core.permissions import BaseRolePermission

class IsWorkLogRoleBasedPermission(BaseRolePermission):
    role_actions = {
        User.Role.DEV: ['list', 'retrieve', 'daily', 'partial_update', 'create'],
        User.Role.ACC: ['list', 'retrieve', 'export', 'daily']
    }

    def has_object_permission(self, request, view, obj):
        allowed = self.role_actions.get(request.user.role, [])
        if not allowed:
            self.logger.warning(f"Undefined role: {request.user.role}")

        if request.user.role == User.Role.PM:
            return True
        if request.user.role == User.Role.DEV:
            if obj.user == request.user:
                return view.action in self.role_actions[User.Role.DEV]

        return False
