from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from gheat_demo.tweetmap.models import TweetPoint

class TweetView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(TweetView, self).get_context_data(**kwargs)
        context.update({'tweet_count':TweetPoint.objects.count()})
        return context
    

urlpatterns = patterns('gheat_demo.tweetmap.views',
    # The basic HTML page that serves as our map view.
    url(r'^$', 
        TweetView.as_view(template_name= getattr(settings,"TWEETMAP_DEFAULT_TEMPLATE","home.html")),
        name    = 'home',
    ),
    url(r'm/^$', 
        TweetView.as_view(template_name= 'home-mobile.html'),
        name    = 'home_mobile',
    ),
    # URL pattern that serves tiles at the path that Google Maps API expects
    # ex.: /tweetmap/tiles/fire/12/3,2.png
    url(
        regex = r'^tiles/(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>\d+),(?P<y>\d+).png$',
        view = 'gheat.views.serve_tile',
        name = 'serve_tile',
    ),
)
