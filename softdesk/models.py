from django.conf import settings
from django.db import models


class Projects(models.Model):
    PROJECT_TYPES = [
        ('B', 'Back-end'),
        ('F', 'Front-end'),
        ('I', 'iOS'),
        ('A', 'Android')
    ]

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    type = models.CharField(choices=PROJECT_TYPES, max_length=9)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return f'[Projects:{self.title}, {self.description}, {self.type}, {self.author_user_id}]'


class Contributors(models.Model):
    CONTRIBUTOR_PERMISSIONS = [
        ('C', "Create"),
        ('R', "Read"),
        ('CR', "Create/Read"),
        ('CRUD', "Create/Read/Update/Delete"),
    ]

    CONTRIBUTOR_ROLES = [
        ('A', 'Author'),
        ('C', 'Contributor')
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(
        max_length=4,
        choices=CONTRIBUTOR_PERMISSIONS,
        default='CRUD',
    )
    role = models.CharField(max_length=11, choices=CONTRIBUTOR_ROLES, default='C')

    class Meta:
        unique_together = (
            "user",
            "project_id",
        )

    def __str__(self):
        return f'[Projects:{self.user}, {self.project_id}, {self.permission}, {self.role}]'


class Issues(models.Model):
    ISSUE_TAGS = [
        ('B', 'Bug'),
        ('M', 'Maintenance'),
        ('U', 'Upgrade')
    ]

    ISSUE_PRIORITIES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High')
    ]

    ISSUE_STATUSES = [
        ('T', 'TBD'),
        ('A', 'Assigned'),
        ('C', 'Close')
    ]
    title = models.CharField(max_length=64)
    desc = models.TextField(max_length=512)
    tag = models.CharField(choices=ISSUE_TAGS, max_length=1)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    priority = models.CharField(choices=ISSUE_PRIORITIES, max_length=5, default='L')
    status = models.CharField(choices=ISSUE_STATUSES, max_length=8, default='T')
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(to=Contributors, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        first_attributes = f'[Issues:{self.title}, {self.desc}, {self.tag}, {self.project_id}, {self.priority},' 
        mid_attributes = f' {self.priority}, {self.status}, {self.author_user_id}, {self.assignee_user_id}'
        last_attributes = f' {self.created_time}]'
        return first_attributes + mid_attributes + last_attributes


class Comments(models.Model):
    description = models.TextField(max_length=512)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[Projects:{self.description}, {self.author_user_id}, {self.issue_id}, {self.created_time}]'

