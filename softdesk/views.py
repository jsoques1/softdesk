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
        my_projects = Contributors.objects.filter(user=self.request.user).values_list('project_id')
        return Projects.objects.filter(id__in=my_projects)

    def perform_create(self, serializer, *args, **kwargs):
        print(f'perform_create:type(request)={type(serializer)}')
        print(f'perform_create:request={serializer}')
        print(f'perform_create:type(self.request)={type(self.request)}')
        print(f'perform_create:self.request={self.request}')
        print(f'perform_create:self.request.user={self.request.user}')
        project_data = serializer.data
        print(f'perform_create:project_data={project_data}')
        author_user = User.objects.get(id=project_data['author_user'])
        print(f'perform_create:author_user={author_user}')
        if self.request.user != author_user:
            raise ValidationError('Requesting user should equal to author_user')

        author_user_id = User.objects.get(id=project_data['author_user'])
        print(f'perform_create:author_user_id.id={author_user_id.id}')
        print(f'perform_create:author_user_id={author_user_id}')
        new_project = Projects.objects.create(title=project_data['title'], description=project_data['description'],
                                              type=project_data['type'], author_user_id=author_user_id.id)
        # new_project.save()
        serializer = ProjectsSerializer(data=project_data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            contributor = Contributors.objects.create(user=author_user, project_id=new_project.id, role='A',
                                                      permission='CRUD')
            # contributor.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        print(f'perform_update:type(request)={type(serializer)}')
        print(f'perform_update:request={serializer}')
        print(f'perform_update:type(self.request)={type(self.request)}')
        print(f'perform_update:self.request={self.request}')
        print(f'perform_update:type(self.request.user)={type(self.request.user)}')
        print(f'perform_update:self.request.user={self.request.user}')

        print(f'self.kwargs={self.kwargs}')

        project_data = self.request.data
        print(f'perform_update:project_data={project_data}')
        author_user = User.objects.get(id=project_data['author_user'])
        print(f"perform_update:author_user.id={author_user.id}")
        if int(self.request.user.id) != int(author_user.id):
            raise ValidationError('Requesting user should equal to author_user')

        # serializer = ProjectsSerializer(data=project_data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
            super().perform_update(serializer, *args, **kwargs)

        instance = self.get_object()  # instance before update
        updated_instance = serializer.save()

    def destroy(self, request, *args, **kwargs):
        print(f'destroy:request.user={self.request.user}')
        print(f'destroy:self.kwargs={self.kwargs}')
        project_id = self.kwargs['pk']
        print(f'destroy:self.kwargs={self.kwargs}')
        authors = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
        if not authors:
            raise ValidationError('Requesting user should be the author')

        print(f'destroy:project_id={project_id}')

        # instance = self.get_object()
        # you custom logic #
        # return super(ProjectsViewSet, self).destroy(request, pk, *args, **kwargs)

        project = self.get_object()
        project.delete()
        return Response({'message': 'Project deleted'}, status=status.HTTP_200_OK)


class ContributorsViewSet(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'get_queryset:request.user={self.request.user}')
        project_id = self.kwargs['projects_pk']
        print(f'project_id={project_id}')
        print(f'self.kwargs={self.kwargs}')
        contributors = Contributors.objects.filter(project=project_id)
        print(f'contributors={contributors}')
        if not contributors:
            raise ValidationError('No contributor found')
        return contributors
        # serializer = ContributorsSerializer(data=contributors, many=True)
        # if serializer.is_valid(raise_exception=True):
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response('Contributors list failed', status=status.HTTP_400_BAD_REQUEST)
        # return super().get_queryset()

    def perform_create(self, serializer, *args, **kwargs):

        print(f'perform_create:type(serializer)={type(serializer)}')
        print(f'perform_create:request={serializer}')
        # print(f'perform_create:request.user.id={request.user.id}')
        print(f'perform_create:type(self.request)={type(self.request)}')
        print(f'perform_create:self.request={self.request}')
        print(f'perform_create:self.request.user={self.request.user}')

        print(f'perform_create:request.user={self.request.data}')
        print(f"self.kwargs={self.kwargs}")
        project_id = self.kwargs.get('projects_pk')
        print(f'project_id={project_id}')
        print(f'type(project_id)={type(project_id)}')
        author = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
        if not author:
            print('not author')
            raise ValidationError('Requesting user is not the project author')
        print(f"type(request.data['project'])={type(serializer.data['project'])}")

        if int(project_id) != int(serializer.data['project']):
            print('not project')
            raise ValidationError('project_id in URL should equal to the form parameter')

        if serializer.data['permission'] != 'CR':
            print('not CR')
            raise ValidationError('permission should be CR')

        print(f"request.data['role']={serializer.data['role']}")
        print(f"type(request.data['role'])={type(serializer.data['role'])}")
        if serializer.data['role'] != 'C':
            print('not C')
            raise ValidationError('role should be C')
        user = User.objects.get(id=serializer.data['user'])
        contributor = Contributors.objects.create(user=user, project_id=project_id, role='C',
                                                  permission='CR')

        print(f'contributor={contributor}')
        print(f'Contributors.objects.all()={Contributors.objects.all()}')
        serializer = ContributorsSerializer(data=serializer.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        print(f'retrieve:request.user={self.request.user}')
        project_id = self.kwargs['projects_pk']
        print(f'self.kwargs={self.kwargs}')
        contributor_id = self.kwargs['pk']
        contributors = Contributors.objects.filter(project=project_id, user=contributor_id)
        if not contributors:
            raise ValidationError('No contributor found')
        print(f'contributors={contributors[0]}')

        contributor = contributors[0]
        serializer = ContributorsSerializer(contributor)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        print(f'destroy:self.kwargs={self.kwargs}')
        print(f'destroy:request.user={self.request.user}')
        project_id = self.kwargs['projects_pk']
        contributor_id = self.kwargs['pk']
        authors = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
        if not authors:
            print(f'authors={authors}')
            raise ValidationError('Requesting user should be the project author')

        if contributor_id == authors[0].user:
            raise ValidationError('Project author can not be deleted')

        contributor = Contributors.objects.get(user=contributor_id)
        contributor.delete()
        return Response({'message': 'Contributor deleted'}, status=status.HTTP_200_OK)


class IssuesViewSet(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'self.kwargs={self.kwargs}')
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('pk')
        if issue_id and project_id:
            queryset = Issues.objects.filter(project=project_id, id=issue_id)
        elif project_id:
            queryset = Issues.objects.filter(project=project_id)
        return queryset
    
    def perform_create(self, serializer, *args, **kwargs):
        # body of target data to be created
        issue_project_id = self.request.data['project']
        assignee_id = self.request.data['assignee_user']
        # current project in the url
        project_id = self.kwargs.get('project_pk')
        # the logged user needs to be member of the project

        if project_id != issue_project_id:
            return Response('project_id is different in the URL and in the form', status=status.HTTP_400_BAD_REQUEST)

        if not Contributors.objects.filter(project_id=project_id, user_id=self.request.user).exists():
            return Response('Requesting user is not a contributor of the project', status=status.HTTP_400_BAD_REQUEST)

        if not Contributors.objects.filter(project_id=project_id, user_id=assignee_id).exists():
            return Response('Assignee is not a contributor of the project', status=status.HTTP_400_BAD_REQUEST)

        super().perform_create(serializer, *args, **kwargs)
        

class CommentsViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'self.kwargs={self.kwargs}')
        # filter the url shown project to members only
        issue_id = self.kwargs.get("issue_pk")
        comment_id = self.kwargs.get("pk")
        if issue_id and comment_id:
            queryset = Comments.objects.filter(id=comment_id)
        elif issue_id:
            queryset = Comments.objects.filter(issue_id=issue_id)
        return queryset

    # def get_queryset(self):
    #     return queryset

