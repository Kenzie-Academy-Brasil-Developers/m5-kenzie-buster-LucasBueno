from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_employee
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        user: User
    ) -> bool:
        if request.user.is_employee or request.user.id == user.id:
            return True
        return False
