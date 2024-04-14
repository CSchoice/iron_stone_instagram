from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    introduce = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images/', blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    created_at = models.DateTimeField(auto_now=True)
