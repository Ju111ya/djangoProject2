from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass


class versSim(models.Model):
    versions = {
        ("4.1", "4.1_custom"),
        ("3.9", "3.9_custom")
    }
    username = models.CharField(max_length=50)
    is_started = models.DateTimeField(default=datetime.now())
    version = models.CharField(max_length=2)

