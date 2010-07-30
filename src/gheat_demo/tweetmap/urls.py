from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from gheat_demo.tweetmap.models import TweetPoint

urlpatterns = patterns('gheat_demo.tweetmap.views',
    # The basic HTML page that serves as our map view.
    url(
        regex   = r'^$',
        view    = direct_to_template, 
        name    = 'home',
        kwargs  = {
            'template': 'home.html',
            'extra_context': {
                'tweet_count':TweetPoint.objects.count()
            }
        }
    ),
    # URL pattern that serves tiles at the path that Google Maps API expects
    # ex.: /tweetmap/tiles/fire/12/3,2.png
    url(
        regex = r'^tiles/(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>\d+),(?P<y>\d+).png$',
        view = 'serve_tile',
        name = 'serve_tile',
    ),
)
