from rest_framework.serializers import ModelSerializer
from .models import Projects, Issues, Comments, Contributors


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
        read_only_fields = ['author_user_id', 'id']


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'
        read_only__fields = ('project_id', 'author_user_id', 'created_time', 'id')


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_only__fields = ('author_user_id', 'issue_id', 'created_time', 'id')


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = '__all__'
        read_only__fields = ('author', 'issue', 'created_time', 'id')



