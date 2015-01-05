# -*- coding: utf-8 -*-
import logging

from django.core.exceptions import MultipleObjectsReturned
from django.views.generic.detail import DetailView

from .models import Photo

logger = logging.getLogger(__name__)


class PhotoDetailView(DetailView):
    model = Photo

    def get_object(self, queryset=None, **kwargs):
        queryset = queryset or self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if slug is None:
            return queryset.last()

        try:
            return queryset.get(slug=slug)
        except MultipleObjectsReturned:
            logger.warning('get_object returned multiple objects for slug %s' % slug)
            return queryset.filter(slug=slug).last()
