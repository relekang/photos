from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from . import settings
from .gallery.views import PhotoDetailView

urlpatterns = [
    url(r'^$', PhotoDetailView.as_view(), name='home'),

    url(r'^archive/', include('photos.gallery.urls', namespace='gallery')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
