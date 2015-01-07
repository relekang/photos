# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import PhotoDetailView, ArchiveView

urlpatterns = patterns(
    '',
    url(r'^$', ArchiveView.as_view(), name='archive'),
    url(r'^last/$', PhotoDetailView.as_view(), name='photo_detail'),
    url(r'^(?P<slug>[^/]+)$', PhotoDetailView.as_view(), name='photo_detail'),
)
