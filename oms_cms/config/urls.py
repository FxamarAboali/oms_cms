"""CMS - DJWOMS
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from oms_cms.backend.urls import urlpatterns as cms_url

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('', include('backend.menu.urls')),
]

urlpatterns += cms_url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "OMS CMS"
admin.site.site_header = "OMS CMS"

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
