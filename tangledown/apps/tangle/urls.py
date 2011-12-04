from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns("tangle.views",
    url(r'^(?P<json_system>.*)$', 'solve'),
)