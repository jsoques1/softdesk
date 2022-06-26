from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from .models import Projects, Issues, Comments, Contributors


class ProjectsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class ContributorsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IssuesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class CommentsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
