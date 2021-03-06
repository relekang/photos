from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views
from .gallery.views import ArchiveView, PhotoDetailView, ArchiveApiView

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^archive/', include('photos.gallery.urls', namespace='gallery')),
    url(r'^api/archive/', ArchiveApiView.as_view()),

    url(r'^u/(?P<username>[a-z0-9]+)/archive/$', ArchiveView.as_view(), name='user_archive'),
    url(r'^api/u/(?P<username>[a-z0-9]+)/archive/$', ArchiveApiView.as_view(),
        name='user_api_archive'),
    url(r'^u/(?P<username>[a-z0-9]+)/$', PhotoDetailView.as_view(), name='user_home'),

    url(r'^admin/', admin.site.urls),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
