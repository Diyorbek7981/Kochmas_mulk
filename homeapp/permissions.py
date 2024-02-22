from rest_framework import permissions
from usersapp.models import ADMIN, MANAGER
from rest_framework.exceptions import ValidationError


class IsAdminOrManangerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.user_roles == ADMIN or request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(obj.owner == request.user or request.user.user_roles == ADMIN or request.user.is_superuser)


class IsOwnerOrReadOnlyPicture(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            obj.home.owner == request.user or request.user.user_roles == ADMIN or request.user.is_superuser)
