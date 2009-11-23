from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

urlpatterns = patterns('home.views',
    url(
        # Example : today/fire/12/3,2.png
        regex = r'^gheat/(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>\d+),(?P<y>\d+).png$',
        view = 'serve_tile',
        name = 'serve_tile',
       ),
    url(
        regex   = r'^home', 
        view    = direct_to_template, 
        name    = 'home',
        kwargs  = {
            'template': 'home.html',
            'extra_context': {
                'google_key':settings.GOOGLE_MAPS_KEY,
                }
            }
    ),
)
