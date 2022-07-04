from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Projects, Issues, Contributors, Comments

from .permissions import ProjectsPermissions, ContributorsPermissions, IssuesPermissions, CommentsPermissions

from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, ContributorsSerializer

User = get_user_model()


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'get_queryset:request.user={self.request.user}')
        print(f'get_queryset:request.user.is_authenticated={self.request.user.is_authenticated}')
        my_projects = Contributors.objects.filter(user=self.request.user).values_list("project_id")
        return Projects.objects.filter(id__in=my_projects)

    def perform_create(self, request, *args, **kwargs):
        if IsAuthenticated:
            print(f'perform_create:IsAuthenticated()={IsAuthenticated()}')
        print(f'perform_create:type(request)={type(request)}')
        print(f'perform_create:request={request}')
        # print(f'perform_create:request.user.id={request.user.id}')
        print(f'perform_create:type(self.request)={type(self.request)}')
        print(f'perform_create:self.request={self.request}')
        print(f'perform_create:self.request.user={self.request.user}')
        print(f'perform_create:self.request.user={self.request.user}')
        project_data = request.data
        print(f'perform_create:project_data={project_data}')
        author_user = User.objects.get(id=project_data['author_user'])
        print(f'perform_create:author_user={author_user}')
        author_user_id = User.objects.get(id=project_data['author_user'])
        print(f'perform_create:author_user_id.id={author_user_id.id}')
        print(f'perform_create:author_user_id={author_user_id}')
        new_project = Projects.objects.create(title=project_data['title'], description=project_data['description'],
                                              type=project_data['type'], author_user_id=author_user_id.id)
        # new_project.save()
        serializer = ProjectsSerializer(data=project_data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            contributor = Contributors.objects.create(user=author_user, project_id=new_project.id, role='A')
            # contributor.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Projects creation failed', status=status.HTTP_400_BAD_REQUEST)


class ContributorsViewSet(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, ContributorsPermissions]

    def get_queryset(self):
        print(f'get_queryset:request.user={self.request.user}')
        project_id = self.kwargs['projects_pk']
        print(f'self.kwargs={self.kwargs}')
        contributors = Contributors.objects.filter(project=project_id)
        print(f'contributors={contributors}')
        if not contributors:
            return Response('No contributor found', status=status.HTTP_204_NO_CONTENT)
        return contributors
        # serializer = ContributorsSerializer(data=contributors, many=True)
        # if serializer.is_valid(raise_exception=True):
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response('Contributors list failed', status=status.HTTP_400_BAD_REQUEST)
        # return super().get_queryset()


class IssuesViewSet(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]


class CommentsViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return queryset

