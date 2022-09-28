from email.policy import default
from pyexpat import model
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


class Poll(models.Model):
    uuid = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)
    firstOption = models.CharField(max_length=255)
    secondOption = models.CharField(max_length=255)
    firstOptionVoteCount = models.IntegerField(default=0)
    secondOptionVoteCount = models.IntegerField(default=0)
    startDate = models.DateField()
    endDate = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.Title


class userPoll(models.Model):
    voted = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return "option voted"
