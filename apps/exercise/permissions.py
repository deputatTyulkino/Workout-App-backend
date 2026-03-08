from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if (request.user and request.user.is_authenticated) or request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (
                request.user == obj.author or
                request.method in SAFE_METHODS
        ) or request.user.is_staff:
            return True
        return False
