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
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'[Projects:{self.id} {self.title}]'


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
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    permission = models.CharField(max_length=4, choices=CONTRIBUTOR_PERMISSIONS)
    role = models.CharField(max_length=11, choices=CONTRIBUTOR_ROLES)

    def __str__(self):
        return f'[Contributors:{self.id} {self.user}]'


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
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    priority = models.CharField(choices=ISSUE_PRIORITIES, max_length=5, default='L')
    status = models.CharField(choices=ISSUE_STATUSES, max_length=8, default='T')
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user = models.ForeignKey(to=Contributors, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        issue_id = f'[Issues:{self.id} {self.title}]'
        return issue_id


class Comments(models.Model):
    description = models.TextField(max_length=512)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[Comments:{self.id} {self.issue}]'

