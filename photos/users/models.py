from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.reverse import reverse


class User(AbstractUser):
    domain = models.CharField(max_length=200, blank=True, db_index=True)

    @property
    def last_photo(self):
        return self.photos.last()

    def get_absolute_url(self):
        if self.domain:
            return "http://{self.domain}".format(self=self)
        return reverse('user_home', args=[self.username])
