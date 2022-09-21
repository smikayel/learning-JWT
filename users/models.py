from django.db import models

# Create your models here.
class User(models.Model):
    uuid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField()

    def __str__(self):
        return self.username