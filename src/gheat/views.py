from django.http import HttpResponse, HttpResponseBadRequest
from gheat import dots, renderer, StorageBackend, color_schemes
from gheat.default_settings import GHEAT_POINT_MODEL

# A bit of foo to dynamically import the Point class
module = '.'.join(GHEAT_POINT_MODEL.split('.')[:-1])
pointclass = GHEAT_POINT_MODEL.split('.')[-1]
Point = getattr(__import__(module, fromlist=[pointclass]), pointclass)


def serve_tile(request,color_scheme,zoom,x,y):
    print 'serve tile:', zoom, x, y
    # Check arguments
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
    
    # Get image and storage backends
    tile = renderer.Tile(Point.objects.all(), color_scheme, dots, zoom, x, y)
    storage_backend = StorageBackend()
    
    # Grab the raw image data
    if tile.is_empty():
        bytes = storage_backend.get_emptytile_bytes(tile)
    else: # tile.is_stale() or ALWAYS_BUILD:
        bytes = storage_backend.get_tile_bytes(tile, 'tweetmap')
    
    # Write the bytes out to the HttpResponse
    return HttpResponse(bytes, content_type="image/png")
