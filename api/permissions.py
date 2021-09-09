from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_teacher or request.method in ["GET"])
