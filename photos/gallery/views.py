# -*- coding: utf-8 -*-
import logging
from django.shortcuts import get_object_or_404

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Photo

logger = logging.getLogger(__name__)


class PhotoDetailView(DetailView):
    model = Photo

    def get_object(self, queryset=None, **kwargs):
        queryset = queryset or self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        host = self.request.get_host()

        if host != 'photos.mocco.no':
            queryset = queryset.filter(user__domain=host)

        if slug is None:
            return queryset.last()
        return get_object_or_404(queryset, slug=slug)


class ArchiveView(ListView):
    model = Photo

    def get_queryset(self):
        queryset = self.model.objects.all()
        host = self.request.get_host()

        if host != 'photos.mocco.no':
            queryset = queryset.filter(user__domain=host)

        return queryset
