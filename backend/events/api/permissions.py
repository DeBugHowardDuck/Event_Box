from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) in ("organizer", "admin")
        )

class IsOrganizerOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True

        user_role = getattr(request.user, "role", None)
        if user_role not in ("organizer", "admin"):
            return False

        owner = getattr(obj, "organizer", None)
        if owner is None and hasattr(obj, "event"):
            owner = obj.event.organizer

        return owner == request.user