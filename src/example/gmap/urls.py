from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('gmap.views',
    (r'^$', 'gmap'),
)
