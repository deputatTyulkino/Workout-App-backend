from rest_framework.permissions import BasePermission


class IsTokenHave(BasePermission):
    def has_permission(self, request, view):
        return request.headers.get('Authorization') is not None

    def has_object_permission(self, request, view, obj):
        return (
                request.user and
                request.user.is_authenticated and
                request.headers.get('Authorization') is not None
        )
