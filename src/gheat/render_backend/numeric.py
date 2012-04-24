import os
from tempfile import SpooledTemporaryFile

import numpy as np
import png

from gheat import SIZE
from gheat import default_settings as gheat_settings
from gheat.opacity import OPAQUE
from gheat.render_backend import base

class ColorScheme(base.ColorScheme):
    def __init__(self, scheme_name, definition_png):
        super(ColorScheme,self).__init__(scheme_name, definition_png)

        image = png.Reader(open(definition_png))
        self.colors = np.array([(r[0], r[1], r[2], r[3]) for r in image.asRGBA()[2]])
        if self.colors.shape != (256, 4):
            raise ValueError, 'Colour scheme must have 256 colours'
        
    def get_empty(self, opacity=OPAQUE):
        color = self.colors[255,:]
        color[3] = int(color[3]*float(opacity)/255)

        empty = np.tile(color, SIZE*SIZE).reshape(SIZE, SIZE*4)

        tmpfile = SpooledTemporaryFile()
        writer = png.Writer(SIZE, SIZE, alpha=True, bitdepth=8)
        writer.write(tmpfile, empty)
        tmpfile.seek(0)
        return tmpfile

def cone(d, x, y):
    # Value is 1.0 when x = d and y = d, and decreases to zero away from this point
    r = np.sqrt((d - x)**2 + (d - y)**2)
    if d == 0:
        if r == 0:
            return 1.0
        else:
            return 0.0
    else:
        return np.max([0.0,  1.0 - r/d])

class Dot(object):
    def __init__(self, zoom):
        self.half_size = int(zoom/2 + 2)
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
        points = self.points()
        
        self.buffer = 2*self.pad
        count = np.zeros([x + 2*self.buffer for x in self.expanded_size])
        density = np.zeros([x + 2*self.buffer for x in self.expanded_size])
        
        # Render the B&W density version of the heatmap
        dot_size = self.dot.shape[0]
        for x, y, weight in points:
            x1 = x + self.buffer - (dot_size - 1)/2
            y1 = y + self.buffer - (dot_size - 1)/2
            count[y1:(y1 + dot_size), 
                x1:(x1 + dot_size)] += self.dot
            density[y1:(y1 + dot_size), 
                x1:(x1+ dot_size)] += self.dot*weight

        # Pick the field to map
        if gheat_settings.GHEAT_MAP_MODE == gheat_settings.GHEAT_MAP_MODE_COUNT:
            img = count
            #opacity = np.zeros(img.shape()) + 255
        elif  gheat_settings.GHEAT_MAP_MODE == gheat_settings.GHEAT_MAP_MODE_SUM_DENSITY:
            img = density
            #opacity = np.clip(count, 0, gheat_settings.GHEAT_OPACITY_LIMIT)
        elif  gheat_settings.GHEAT_MAP_MODE == gheat_settings.GHEAT_MAP_MODE_MEAN_DENSITY:
            img = density
            img[count > 0] /= count[count > 0]
            #opacity = np.clip(count, 0, gheat_settings.GHEAT_OPACITY_LIMIT)
        else:
            raise ValueError, 'Unknown map mode'
            
        # Crop resulting density image (which could have grown) into the
        # actual canvas size we want
        img = img[(self.pad + self.buffer):(SIZE + self.pad + self.buffer), 
            (self.pad + self.buffer):(SIZE + self.pad + self.buffer)]
        #opacity = opacity[self.pad:(SIZE + self.pad), self.pad:(SIZE + self.pad)]

        # Convert to a 0 to 255 image
        img = np.clip(256.0*np.power(img/gheat_settings.GHEAT_MAX_VALUE, 
            gheat_settings.GHEAT_SCALING_COEFFICIENT), 0, 255.999).astype('uint8')
        

        # Given the B&W density image, generate a color heatmap based on
        # this Tile's color scheme.
        colour_image = np.zeros((SIZE, SIZE, 4), 'uint8')
        for i in range(4):
            colour_image[:,:,i] = self.schemeobj.colors[:,i][255 - img]
        
        tmpfile = SpooledTemporaryFile()
        writer = png.Writer(SIZE, SIZE, alpha=True, bitdepth=8)
        writer.write(tmpfile, np.reshape(colour_image, (SIZE, SIZE*4)))
        tmpfile.seek(0)
        return tmpfile
