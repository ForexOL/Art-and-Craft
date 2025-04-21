from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from . import settings

from django.views.static import serve
from django.conf.urls import (
                                handler400,
                                handler403,
                                handler404,
                                handler500)

from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from shop.sitemaps import StaticViewSitemap#, ProductSitemap #


sitemaps = {'static': StaticViewSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),  # Include shop routes
    path('/payments/', include('django_pesapalv3.urls')),  # Pesapal v3 endpoints
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]
#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)


handler400 = 'shop.views.views.bad_request'
handler403 = 'shop.views.views.permission_denied'
handler404 = 'shop.views.views.page_not_found'
handler500 = 'shop.views.views.server_error'
