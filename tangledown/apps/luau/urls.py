from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("luau.views",
    url(r'^$', 'show_page'),
    url(r'^(?P<page_slug>[^/]*)/$', 'show_page'),
    url(r'^(?P<page_slug>[^/]*)/edit/$', 'edit_page'),
)