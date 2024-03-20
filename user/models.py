from django.contrib.auth.models import AbstractUser
from django.db import models
from user.managers import CustomUserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatar', blank=True)

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
