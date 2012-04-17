from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings


urlpatterns = patterns('home.views',
    url(
        regex   = r'', 
        view    = direct_to_template, 
        name    = 'home',
        kwargs  = {
            'template': 'home.html',
            }
        ),
)
