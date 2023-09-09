from rest_framework import permissions


class IsNotSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_superuser)
