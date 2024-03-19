from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=256, blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    avatar = models.ImageField(upload_to='')  # Where
    last_name = None
    first_name = None
    is_active = True

    REQUIRED_FIELDS = ['email', 'password']


class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_roadmaps = models.IntegerField()
    completed_roadmaps = models.IntegerField()
    in_progress_roadmaps = models.IntegerField()
