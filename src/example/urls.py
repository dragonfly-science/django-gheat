from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^$', 'django.views.generic.simple.redirect_to', {'url' : '/gmap/'}),
    (r'^gmap/', include('gmap.urls')),
    (r'^tiles/', include('gheat.urls')),
)

