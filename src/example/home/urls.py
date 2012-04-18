from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.conf import settings


urlpatterns = patterns('home.views',
    (r'^$', TemplateView.as_view(template_name= 'home.html')),
)
