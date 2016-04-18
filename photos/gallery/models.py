# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from PIL import Image
from PIL.ExifTags import TAGS
from thumbnails import get_thumbnail


def photo_upload_to(instance, filename):
    return 'photos/user_{0}/{1}'.format(instance.user.id, filename)


class Photo(models.Model):
    user = models.ForeignKey('users.User', related_name='photos')
    file = models.ImageField(upload_to=photo_upload_to)
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=160, db_index=True, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'slug']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "{0}/archive/{1}".format(self.user.get_absolute_url(), self.slug)

    @property
    def large_thumbnail(self):
        return get_thumbnail(self.file.path, '3000')

    @property
    def medium_thumbnail(self):
        return get_thumbnail(self.file.path, '1000')

    @property
    def archive_thumbnail(self):
        return self.square_thumbnail('500x500')

    def square_thumbnail(self, size='1000x1000'):
        return get_thumbnail(self.file.path, size, crop='center')

    @property
    def admin_thumbnail(self):
        return mark_safe('<img src="{}" alt="{}" />'.format(
            get_thumbnail(self.file.path, '150').url,
            self.title
        ))

    @property
    def camera(self):
        return self.exif.get('Model')

    @property
    def lens(self):
        return self.exif.get('LensModel')

    @property
    def exposure_time(self):
        return '{}/{}'.format(self.exif.get('ExposureTime')[0], self.exif.get('ExposureTime')[1])

    @property
    def aperture(self):
        return self.exif.get('FNumber')[0] / self.exif.get('FNumber')[1]

    @property
    def focal_length(self):
        return int(self.exif.get('FocalLength')[0] / self.exif.get('FocalLength')[1])

    @property
    def iso(self):
        return self.exif.get('ISOSpeedRatings')

    @cached_property
    def exif(self):
        key = 'photoexif{}'.format(self.pk)
        data = cache.get(key)
        if data is None:
            with Image.open(self.file) as image:
                exif = image._getexif()
            data = {}
            for key in exif:
                data[TAGS.get(key, key)] = exif[key]
            cache.set(key, data)
        return data
