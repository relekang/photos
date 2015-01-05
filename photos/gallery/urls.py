# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import PhotoDetailView

urlpatterns = patterns(
    '',
    url(r'^$', PhotoDetailView.as_view(), name='photo_detail'),
    url(r'^(?P<slug>[^/]+)$', PhotoDetailView.as_view(), name='photo_detail'),
)
