from rest_framework.permissions import BasePermission

class IsCheckerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_staff:
            return True
        return getattr(request.user, 'role', None) in ("checkin", "admin")