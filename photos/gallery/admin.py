# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'file', 'taken_at', 'camera', 'lens',
                    'focal_length', 'exposure_time', 'aperture', 'iso')
    date_hierarchy = 'taken_at'
