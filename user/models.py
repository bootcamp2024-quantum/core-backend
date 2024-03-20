from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    avatar = models.ImageField(upload_to='user_avatar', blank=True)

    REQUIRED_FIELDS = ['email']
