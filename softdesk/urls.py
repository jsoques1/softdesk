from rest_framework_nested import routers
# from rest_framework import routers
from django.urls import path, include

from .views import ProjectsViewSet, ContributorsViewSet, IssuesViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register('projects', ProjectsViewSet, basename='projects')

projects = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
projects.register('users', ContributorsViewSet, basename='users')
projects.register('issues', IssuesViewSet, basename='issues')

issues = routers.NestedSimpleRouter(projects, r'issues', lookup='issues')
issues.register('comments', CommentsViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects.urls)),
    path('', include(issues.urls)),
]