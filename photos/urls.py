from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from photos import settings
from photos.gallery.views import PhotoDetailView

urlpatterns = patterns(
    '',
    url(r'^$', PhotoDetailView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

