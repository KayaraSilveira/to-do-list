from django.contrib.auth.models import User
from django.db import models


class ListTasks(models.Model):
    title = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name='list_members')

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    list_tasks = models.ForeignKey(ListTasks, on_delete=models.CASCADE)
    order_home = models.IntegerField(null=True)
    order_list = models.IntegerField(null=True)

    def __str__(self):
        return self.title
