from django.shortcuts import render_to_response
from gheat.models import Point

from django.conf import settings

def gmap(request):
    extent = Point.objects.all().extent()
    print extent
    return render_to_response('gmap.html', {'extent': extent, 'api_key': settings.GOOGLEMAPS_API_KEY})

    
