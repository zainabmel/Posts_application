from django.db import models
from django.contrib.auth.models import AbstractUser #to extend the default user created by django

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None #overwrite the requierd username attribute to None because we want to login using the email instead
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

