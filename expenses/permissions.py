from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """ Custom permission to only allow owners of an object to edit it. """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsManager(permissions.BasePermission):
    """ Custom permission to only allow managers to perform certain actions. """
    def has_permission(self, request, view):
        return request.user.profile.role == 'manager'