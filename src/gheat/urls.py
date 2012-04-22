from django.conf.urls.defaults import *

urlpatterns = patterns('gheat.views',
    url(r'^(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>-?\d+),(?P<y>-?\d+).png$',
        'serve_tile', name = 'serve_tile'),
)

