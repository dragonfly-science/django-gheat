import os
from tempfile import SpooledTemporaryFile

import numpy as np
from PIL import Image, ImageChops
import png

from gheat import SIZE
from gheat import default_settings as gheat_settings
from gheat.opacity import OPAQUE
from gheat.render_backend import base

class ColorScheme(base.ColorScheme):
    def __init__(self, schemename, definition_png):
        super(ColorScheme,self).__init__(schemename, definition_png)
        
        self.colors = Image.open(definition_png).load()

    def get_empty(self, opacity=OPAQUE):
        color = self.colors[0, 255]
        if (type(color) is not int) and (len(color) == 4): # color map has per-pixel alpha
            (conf, pixel) = opacity, color[3] 
            opacity = int(( (conf/255.0)    # from configuration
                          * (pixel/255.0)   # from per-pixel alpha
                           ) * 255)

        if (type(color) is not int):
            color = color[:3] + (opacity,)
        
        tile = Image.new('RGBA', (SIZE, SIZE), color)
        
        tmpfile = SpooledTemporaryFile()
        tile.save(tmpfile, 'PNG')
        tmpfile.seek(0)
        
        return tmpfile

#class Dot(base.Dot):
#    def __init__(self, zoom):
#        super(Dot, self).__init__(zoom)
#        self.img = Image.open(self.definition_png)
#        self.half_size = (self.img.size[0] / 2)

def cone(d, x, y):
    # Value is 1 when x = d and y = d, and decreases to zero away from this point
    r = np.sqrt((d - x)**2 + (d - y)**2)
    return np.max([0,  1 - r/d])

class Dot(object):
    def __init__(self, zoom):
        self.half_size = zoom
        self.img = np.zeros((self.half_size*2 + 1, self.half_size*2 + 1))
        self.size = self.img.shape[0]
        for i in range(self.size):
            for j in range(self.size):
                self.img[i, j] = cone(self.half_size, i, j)

class Tile(base.Tile):
    def __init__(self, queryset, color_scheme, dots, zoom, x, y, point_field='geometry', last_modified_field=None, density_field=None):
        super(Tile, self).__init__(queryset, color_scheme, dots, zoom, x, y, point_field, last_modified_field, density_field)
        
        _color_schemes_dir = os.path.join(gheat_settings.GHEAT_CONF_DIR, 'color-schemes')
        self.schemeobj = ColorScheme(
            self.color_scheme,
            os.path.join(_color_schemes_dir, "%s.png" % self.color_scheme)
        )

    def generate(self):
        print 'Generate tile', len(self.points())
        points = self.points()
        
        # Grab a new PIL image canvas
        count = np.zeros(self.expanded_size)
        density = np.zeros(self.expanded_size)
        
        # Render the B&W density version of the heatmap
        size = self.dot.shape[0]
        half_size = (size - 1)/2

        for y, x, weight in points:
            count[x:(x + size), y:(y + size)] += self.dot
            density[x:(x + size), y:(y + size)] += self.dot*weight


        # Pick the field to map
        if gheat_settings.GHEAT_MAP_MODE == gheat_settings.GHEAT_MAP_MODE_COUNT:
            img = count
            #opacity = np.zeros(img.shape()) + 255
        elif  gheat_settings.GHEAT_MAP_MODE == gheat_settings.GHEAT_MAP_MODE_SUM_DENSITY:
            img = density
            #opacity = np.clip(count, 0, gheat_settings.GHEAT_OPACITY_LIMIT)
        elif  gheat_settings.GHEAT_MAP_MODE == gheat_settings.GHEAT_MAP_MODE_MEAN_DENSITY:
            img = density/count
            #opacity = np.clip(count, 0, gheat_settings.GHEAT_OPACITY_LIMIT)
        else:
            raise ValueError, 'Unknown map mode'
            
        # Crop resulting density image (which could have grown) into the
        # actual canvas size we want
        img = img[self.pad:(SIZE + self.pad), self.pad:(SIZE + self.pad)]
        #opacity = opacity[self.pad:(SIZE + self.pad), self.pad:(SIZE + self.pad)]

        # Convert to a 0 to 255 image
        img = np.clip(256.0*np.power(img/gheat_settings.GHEAT_MAX_VALUE, gheat_settings.GHEAT_SCALING_COEFFICIENT), 0, 255.999).astype('uint8')
        
        # Given the B&W density image, generate a color heatmap based on
        # this Tile's color scheme.
        _computed_opacities = dict()
        colour_image = np.zeros((SIZE, SIZE, 4), 'uint8')
        img = 255 - img
        for x in range(SIZE):
            for y in range(SIZE):

                # Get color for this intensity
                # ============================
                # is a value
                val = self.schemeobj.colors[0, int(img[x, y])]
                try:
                    pix_alpha = val[3] # the color image has transparency
                except IndexError:
                    pix_alpha = OPAQUE # it doesn't
                

                # Blend the opacities
                # ===================
                conf, pixel = self.opacity, pix_alpha
                if (conf, pixel) not in _computed_opacities:
                    opacity = int(( (conf/255.0)    # from configuration
                                  * (pixel/255.0)   # from per-pixel alpha
                                   ) * 255)
                    _computed_opacities[(conf, pixel)] = opacity

                
                colour_image[x, y, :] = val[:3] + (_computed_opacities[(conf, pixel)],)

        tmpfile = SpooledTemporaryFile()
        writer = png.Writer(SIZE, SIZE, alpha=True, bitdepth=8)
        writer.write(tmpfile, np.reshape(colour_image, (SIZE, SIZE*4)))

        #writer.write(tmpfile, img)
        tmpfile.seek(0)
       
        return tmpfile
