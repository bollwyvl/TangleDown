from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", 'views.home', name='home'),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^wiki/', include('luau.urls')),
    url(r'^tangle/', include('tangle.urls')),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', 
        {'url': '%simg/favicon.ico' % settings.STATIC_URL}),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
