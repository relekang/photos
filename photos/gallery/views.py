# -*- coding: utf-8 -*-
import logging

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from photos.users.models import User
from .models import Photo

logger = logging.getLogger(__name__)


class PhotoViewMixin(object):
    model = Photo

    def dispatch(self, *args, **kwargs):
        username = self.kwargs.get('username', None)
        host = self.request.get_host()

        # if host != 'photos.mocco.no' and host != '127.0.0.1:8000':
        #     raise Http404()

        if username:
            user = User.objects.get(username=username)
            if user.domain:
                return redirect("http://{domain}{path}".format(
                    domain=user.domain,
                    path=self.request.get_full_path().replace(r'^/u/{0}'.format(username), '')
                ))

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username', None)
        host = self.request.get_host()

        if host != 'photos.mocco.no' and host != '127.0.0.1:8000':
            context['photographer'] = User.objects.get(domain=host)
        elif username:
            context['photographer'] = User.objects.get(username=username)
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        host = self.request.get_host()
        username = self.kwargs.get('username', None)

        if host != 'photos.mocco.no' and host != '127.0.0.1:8000':
            queryset = queryset.filter(user__domain=host)
        elif username is not None:
            queryset = queryset.filter(user__username=username)

        return queryset


class PhotoDetailView(PhotoViewMixin, DetailView):
    def get_object(self, queryset=None, **kwargs):
        queryset = queryset or self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if slug is None:
            return queryset.last()
        return get_object_or_404(queryset, slug=slug)


class ArchiveView(PhotoViewMixin, ListView):
    pass
