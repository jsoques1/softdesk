from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from .models import Projects, Issues, Comments, Contributors


class ProjectsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f'request.user={request.user}')
        print(f'type(request.user)={type(request.user)}')
        print(f'request.user.is_authenticated()={bool(request.user.is_authenticated)}')
        print(f'view={view}')
        return True


class ContributorsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f'view.kwargs={view.kwargs}')
        print(f'request.method={request.method}')
        print(f'permissions.SAFE_METHODS={permissions.SAFE_METHODS}')

        project = get_object_or_404(Projects, id=view.kwargs['projects_pk'])
        if request.method in permissions.SAFE_METHODS:
            print('request.method in permissions.SAFE_METHODS')
            retval = project in Projects.objects.filter(contributors__user=request.user)
            print(f'retval={retval}')
            return project in Projects.objects.filter(contributors__user=request.user)
        print('NOT request.method in permissions.SAFE_METHODS')
        return request.user == project.author_user

    def has_object_permission(self, request, view, obj):
        print(f'view.kwargs={view.kwargs}')
        return True


class IssuesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class CommentsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
