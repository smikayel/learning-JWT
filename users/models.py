from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(models.Model):
    uuid = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField()

    def __str__(self):
        return self.username