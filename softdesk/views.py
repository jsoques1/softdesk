from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Projects, Issues, Contributors, Comments

from .serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, ContributorsSerializer

User = get_user_model()


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        my_projects = Contributors.objects.filter(user=self.request.user).values_list('project_id')
        return Projects.objects.filter(id__in=my_projects)

    def perform_create(self, serializer, *args, **kwargs):
        project_data = serializer.data
        author_user = User.objects.get(id=project_data['author_user'])
        if self.request.user != author_user:
            raise ValidationError('Requesting user should equal to author_user')

        author_user_id = User.objects.get(id=project_data['author_user'])
        new_project = Projects.objects.create(title=project_data['title'], description=project_data['description'],
                                              type=project_data['type'], author_user_id=author_user_id.id)
        serializer = ProjectsSerializer(data=project_data)
        if serializer.is_valid(raise_exception=True):
            contributor = Contributors.objects.create(user=author_user, project_id=new_project.id, role='A',
                                                      permission='CRUD')
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        project_data = self.request.data
        author_user = User.objects.get(id=project_data['author_user'])
        if int(self.request.user.id) != int(author_user.id):
            raise ValidationError('Requesting user should equal to author_user')

        comment = self.get_object()
        if int(self.request.user.id) != int(comment.author_user_id):
            raise ValidationError('Requesting user {self.request.user.username} is not the project author')

        instance = self.get_object()  # instance before update
        updated_instance = serializer.save()

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        authors = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
        if not authors:
            raise ValidationError('Requesting user should be the project author')

        project = self.get_object()
        project.delete()
        return Response({'message': 'Project deleted'}, status=status.HTTP_200_OK)


class ContributorsViewSet(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['projects_pk']

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        contributors = Contributors.objects.filter(project=project_id)

        return contributors

    def perform_create(self, serializer, *args, **kwargs):
        project_id = self.kwargs.get('projects_pk')
        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        author = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
        if not author:
            raise ValidationError(f'Requesting user {self.request.user.username} is not the project author')

        if int(project_id) != int(serializer.data['project']):
            raise ValidationError(f'project_id in URL {project_id} should equal to the form parameter')

        if serializer.data['permission'] != 'CR':
            raise ValidationError('permission should be CR')

        if serializer.data['role'] != 'C':
            raise ValidationError('role should be C')
        user = User.objects.get(id=serializer.data['user'])
        contributor = Contributors.objects.create(user=user, project_id=project_id, role='C',
                                                  permission='CR')

        serializer = ContributorsSerializer(data=serializer.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        project_id = self.kwargs['projects_pk']
        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        contributor_id = self.kwargs['pk']
        contributors = Contributors.objects.filter(project=project_id, id=contributor_id)
        if not contributors:
            raise ValidationError(f'Contributor {contributor_id} for project {project_id} does not exist')

        contributor = contributors[0]
        serializer = ContributorsSerializer(contributor)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['projects_pk']

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        contributor_id = self.kwargs['pk']

        if not Contributors.objects.filter(id=contributor_id).exists():
            raise ValidationError(f'Contributor {contributor_id} for project {project_id} does not exist')

        authors = Contributors.objects.filter(project=project_id, user=self.request.user, role='A')
        if not authors:
            raise ValidationError(f'Requesting user {self.request.user.username} is not the project author')

        if int(contributor_id) == int(authors[0].id):
            raise ValidationError(f'Author {contributor_id} for project {project_id} can not be deleted')

        contributor = self.get_object()
        contributor.delete()
        return Response({'message': 'Contributor deleted'}, status=status.HTTP_200_OK)


class IssuesViewSet(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('projects_pk')

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        queryset = Issues.objects.filter(project=project_id)
        return queryset

    def perform_create(self, serializer, *args, **kwargs):
        project_id = self.kwargs.get('projects_pk')

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        issue_project_id = self.request.data['project']

        if int(project_id) != int(issue_project_id):
            raise ValidationError(f'project_id {project_id} is different in the URL and in the form')

        if not Contributors.objects.filter(project_id=project_id, user_id=self.request.user).exists():
            raise ValidationError(f'Requesting user {self.request.user.username} is not a contributor of the project')

        issue_data = self.request.data
        author_user = User.objects.get(id=issue_data['author_user'])
        if int(self.request.user.id) != int(author_user.id):
            raise ValidationError('Requesting user should equal to author_user')

        contributor_id = issue_data['assignee_user']
        if not Contributors.objects.filter(project_id=project_id, id=contributor_id).exists():
            raise ValidationError(f'Assignee_user {contributor_id} is not a contributor of the project')

        assignee_user_id = Contributors.objects.get(id=contributor_id)

        serializer = ProjectsSerializer(data=issue_data)
        if serializer.is_valid(raise_exception=True):
            issue = Issues.objects.create(title=issue_data['title'], desc=issue_data['desc'], tag=issue_data['tag'],
                                          project_id=project_id, priority=issue_data['priority'],
                                          status=issue_data['status'], author_user_id=author_user.id,
                                          assignee_user_id=assignee_user_id.id,
                                          created_time=timezone.now())

            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        project_id = self.kwargs.get('projects_pk')

        issue_project_id = self.request.data['project']

        if int(project_id) != int(issue_project_id):
            raise ValidationError(f'project_id {project_id} is different in the URL and in the form')

        issue_data = self.request.data
        author_user = User.objects.get(id=issue_data['author_user'])
        if int(self.request.user.id) != int(author_user.id):
            raise ValidationError('Requesting user should equal to author_user')

        contributor_id = issue_data['assignee_user']
        if not Contributors.objects.filter(project_id=project_id, id=contributor_id).exists():
            raise ValidationError(f'Assignee_user {contributor_id} is not a contributor of the project')

        instance = self.get_object()  # instance before update
        updated_instance = serializer.save()

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs['projects_pk']

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        issue_id = self.kwargs['pk']

        if not Issues.objects.filter(id=issue_id).exists():
            raise ValidationError(f'Issue {issue_id} for project {project_id} does not exist')

        issue = Issues.objects.get(id=issue_id)
        if int(self.request.user.id) != int(issue.author_user.id):
            raise ValidationError(f'Requesting user {self.request.user.username} is not the issue author')

        issue = self.get_object()
        issue.delete()
        return Response({'message': 'Issue deleted'}, status=status.HTTP_200_OK)


class CommentsViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('projects_pk')

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        issue_id = self.kwargs.get("issues_pk")
        if not Issues.objects.filter(id=issue_id).exists():
            raise ValidationError(f'Issue_id {issue_id} does not exist')

        queryset = Comments.objects.filter(issue=issue_id)
        return queryset

    def perform_create(self, serializer, *args, **kwargs):
        project_id = self.kwargs.get('projects_pk')

        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        issue_id = self.kwargs.get("issues_pk")
        if not Issues.objects.filter(id=issue_id).exists():
            raise ValidationError(f'Issue_id {issue_id} does not exist')

        comment_data = self.request.data

        if int(issue_id) != int(comment_data['issue']):
            raise ValidationError(f'issue_id {issue_id} is different in the URL and in the form')

        author_user_id = User.objects.get(id=comment_data['author_user'])

        serializer = CommentsSerializer(data=comment_data)
        if serializer.is_valid(raise_exception=True):
            issue = Comments.objects.create(description=comment_data['description'],
                                            author_user_id=comment_data['author_user'],
                                            issue_id=comment_data['issue'])
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        project_id = self.kwargs.get('projects_pk')
        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        issue_id = self.kwargs.get("issues_pk")
        if not Issues.objects.filter(id=issue_id).exists():
            raise ValidationError(f'Issue_id {issue_id} does not exist')

        comment_data = self.request.data

        if int(issue_id) != int(comment_data['issue']):
            raise ValidationError(f'issue_id {issue_id} is different in the URL and in the form')

        author_user_id = User.objects.get(id=comment_data['author_user'])

        comment = self.get_object()
        if int(self.request.user.id) != int(comment.author_user_id):
            raise ValidationError(f'Requesting user {self.request.user.username} is not the comment author')

        if int(comment.author_user_id) != int(author_user_id.id):
            raise ValidationError('Can not change the comment author')

        instance = self.get_object()  # instance before update
        updated_instance = serializer.save()

    def destroy(self, request, *args, **kwargs):
        project_id = self.kwargs.get('projects_pk')
        if not Projects.objects.filter(id=project_id).exists():
            raise ValidationError(f'Project {project_id} does not exist')

        issue_id = self.kwargs.get("issues_pk")
        if not Issues.objects.filter(id=issue_id).exists():
            raise ValidationError(f'Issue_id {issue_id} does not exist')

        comment = self.get_object()
        if int(self.request.user.id) != int(comment.author_user_id):
            raise ValidationError(f'Requesting user {self.request.user.username} is not the comment author')

        comment.delete()
        return Response({'message': 'Comment deleted'}, status=status.HTTP_200_OK)