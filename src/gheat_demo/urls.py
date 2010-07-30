from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url' : '/tweetmap/'}),
    (r'^tweetmap/', include('gheat_demo.tweetmap.urls')),
)
