from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=64)
    description = models.CharField(max_length=264)

    def __str__(self):
        return self.group
        

class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    front = models.CharField(max_length=64)
    back = models.CharField(max_length=128)
    revision = models.DateField()
    factor = models.IntegerField(max_length=12, default=0)

    def __str__(self):
        return self.front