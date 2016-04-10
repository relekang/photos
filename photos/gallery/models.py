# -*- coding: utf-8 -*-
from PIL import Image
from PIL.ExifTags import TAGS
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from sorl.thumbnail import get_thumbnail


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

    @property
    def large_thumbnail(self):
        return get_thumbnail(self.file, '3000')

    @property
    def archive_thumbnail(self):
        return self.square_thumbnail('500x500')

    def square_thumbnail(self, size='1000x1000'):
        return get_thumbnail(self.file, size, crop='center')

    @property
    def admin_thumbnail(self):
        return mark_safe('<img src="{}" alt="{}" />'.format(
            get_thumbnail(self.file, '150').url,
            self.title
        ))

    @property
    def camera(self):
        return self.exif['Model']

    @property
    def lens(self):
        return self.exif['LensModel']

    @property
    def exposure_time(self):
        return '{}/{}'.format(self.exif['ExposureTime'][0], self.exif['ExposureTime'][1])

    @property
    def aperture(self):
        return self.exif['FNumber'][0] / self.exif['FNumber'][1]

    @property
    def focal_length(self):
        return int(self.exif['FocalLength'][0] / self.exif['FocalLength'][1])

    @property
    def iso(self):
        return self.exif['ISOSpeedRatings']

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
