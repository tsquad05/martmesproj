
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from django.views.generic.base import TemplateView
from core.sitemaps import StaticSitemap, CategorySitemap, ProductSitemap
#Sitemaps
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticSitemap,
    'Category': CategorySitemap,
    'Product': ProductSitemap,
}

context = {
    'sitemaps': sitemaps
}
urlpatterns = [

    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("userauths.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('sitemap.xml/', sitemap, context, name="django.contrib.sitemaps.views.sitemap"),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'core.views.error_400'
handler404 = 'core.views.error_404'
handler403 = 'core.views.error_403'
handler500 = 'core.views.error_500'
