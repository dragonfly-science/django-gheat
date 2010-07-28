from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url' : '/friends/'}),
    (r'^friends/', include('gheat_demo.friends.urls')),
)
