from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from . import settings

from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),  # Include shop routes
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
