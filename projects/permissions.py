# projects/permissions.py
from rest_framework import permissions


class IsProjectOwner(permissions.BasePermission):
    """Allows access only to project owners."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsProjectManager(permissions.BasePermission):
    """Allows access to users with the Project Manager role."""

    def has_object_permission(self, request, view, obj):
        return obj.projectmembership_set.filter(user=request.user, role='Project Manager').exists()


class IsMember(permissions.BasePermission):
    """Allows access to users with the Member role."""

    def has_object_permission(self, request, view, obj):
        return obj.projectmembership_set.filter(user=request.user, role__in=['Member', 'Project Manager']).exists()


class IsViewer(permissions.BasePermission):
    """Allows read-only access to users with the Viewer role."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.projectmembership_set.filter(user=request.user, role__in=['Viewer', 'Member', 'Project Manager']).exists() or obj.is_public
