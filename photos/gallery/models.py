# -*- coding: utf-8 -*-
from django.db import models
from sorl.thumbnail import get_thumbnail


class Photo(models.Model):
    file = models.ImageField(upload_to='photos')
    title = models.CharField(max_length=150)
    taken_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file.name

    @property
    def large_thumbnail(self):
        return get_thumbnail(self.file, '3000')

    @property
    def square_thumbnail(self):
        return get_thumbnail(self.file, '1000x1000', crop='center')
