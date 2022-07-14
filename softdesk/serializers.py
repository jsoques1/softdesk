from rest_framework.serializers import ModelSerializer
from .models import Projects, Issues, Comments, Contributors


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = '__all__'
