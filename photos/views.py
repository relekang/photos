from django.shortcuts import render

from photos.gallery.views import PhotoDetailView

from .users.models import User


def index(request):
    if request.get_host() == 'photos.mocco.no' or request.get_host() == '127.0.0.1:8000':
        return render(request, 'index.html', {
            'users': User.objects.filter(is_active=True)
        })
    return PhotoDetailView.as_view()(request)
