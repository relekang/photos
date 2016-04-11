from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    domain = models.CharField(max_length=200, blank=True, db_index=True)
