from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^$', 'django.views.generic.simple.redirect_to', {'url' : '/gmap/'}),
    (r'^gmap/', include('gmap.urls')),
    url(
        # Example : today/fire/12/3,2.png
        regex = r'^tiles/(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>\d+),(?P<y>\d+).png$',
        view = 'gheat.views.serve_tile',
        name = 'serve_tile',
    ),
)

