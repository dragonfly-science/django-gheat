from django.shortcuts import render_to_response
from gheat.models import Point

def gmap(request):
    extent = Point.objects.all().extent()
    return render_to_response('gmap.html', {'extent': extent})

    
