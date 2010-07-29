import os.path
from django.http import HttpResponse
from gheat import dots, renderer, storage, color_schemes, translate, log, \
        ALWAYS_BUILD

from django.http import HttpResponseBadRequest
from django.conf import settings
from django.views.static import serve

from gheat_demo.friends.models import FriendPoint

# Create your views here.
def serve_tile(request,color_scheme,zoom,x,y):
    '''
        Responsible for serving png files of the tile for the heat map

        This view will try to serve the file from the filesystem in case already
        exists otherwise just try to genereate it, and serve it.
    '''

    # Asserting request is a correct one
    try:
        assert color_scheme in color_schemes, ( "bad color_scheme: "
                                              + color_scheme
                                               )
        assert zoom.isdigit() and x.isdigit() and y.isdigit(), "not digits"
        zoom = int(zoom)
        x = int(x)
        y = int(y)
        assert 0 <= zoom <= 30, "bad zoom: %d" % zoom
    except AssertionError, err:
        return HttpResponseBadRequest()

    
    
    bytes = generate_tile(request,color_scheme,zoom,x,y)
    return HttpResponse(bytes, content_type="image/png")


def generate_tile(request,color_scheme,zoom,x,y):
    '''
        This view will generate the png file for the current request
    '''
    tile = renderer.Tile(FriendPoint.objects.all(), color_scheme, dots, zoom, x, y)
    
    storage_backend = storage()
    
    if tile.is_empty():
        bytes = storage_backend.get_emptytile_bytes(tile)
    else: # tile.is_stale() or ALWAYS_BUILD:
        bytes = storage_backend.get_tile_bytes(tile, 'friendmap')

    return bytes
