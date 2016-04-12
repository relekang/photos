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

    def custom_domain(self):
        host = self.request.get_host()
        return host != 'photos.mocco.no' and host != '127.0.0.1:8000'

    def dispatch(self, *args, **kwargs):
        username = self.kwargs.get('username', None)

        if username and self.custom_domain():
            raise Http404()

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

        if self.custom_domain():
            context['photographer'] = User.objects.get(domain=self.request.get_host())
        elif username:
            context['photographer'] = User.objects.get(username=username)
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        username = self.kwargs.get('username', None)

        if self.custom_domain():
            queryset = queryset.filter(user__domain=self.request.get_host())
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
