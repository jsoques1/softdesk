from rest_framework import routers
from . import views
from django.urls import path, include

from .views import ProjectsViewSet, ContributorsViewSet, IssuesViewSet, CommentsViewSet

router = routers.SimpleRouter()
router.register("projects", ProjectsViewSet, basename="projects")
router.register("users", ContributorsViewSet, basename="users")
router.register("issues", IssuesViewSet, basename="issues")
router.register("comments", CommentsViewSet, basename="comments")

urlpatterns = [
    path('api/', include(router.urls))
]