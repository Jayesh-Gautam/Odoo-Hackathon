from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.ADMIN)

class IsManager(BasePermission):
    """
    Allows access only to manager users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.MANAGER)

class IsEmployee(BasePermission):
    """
    Allows access only to employee users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.EMPLOYEE)
