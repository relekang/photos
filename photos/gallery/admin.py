# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('admin_thumbnail', 'title', 'file', 'taken_at', 'camera', 'lens',
                    'focal_length', 'exposure_time', 'aperture', 'iso')
    date_hierarchy = 'taken_at'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id

        if not request.user.is_superuser:
            kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
