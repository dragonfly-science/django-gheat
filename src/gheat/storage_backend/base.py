class BaseStorage(object):
    """
    Dummy storage class, which defines the API for storage backends. This is usable
    as-is, although tiles are never stored/cached.
    """
    def has_tile(self, tile, mapname=""):
        """
        Subclasses should actually implement this so that tiles are not generated on
        every call.
        """
        return False
        
    def get_tile(self, tile, mapname=""):
        """
        Returns the given tile as a file-like object representing PNG image data.
        """
        return tile.generate()
    
    def get_tile_bytes(self, tile, mapname=""):
        """
        Returns the given tile as raw binary PNG data.
        """
        return self.get_tile(tile, mapname).read()
    
    def get_emptytile(self, tile):
        """
        Returns the 'empty tile' a file-like object.
        """
        return tile.get_empty()
    
    def get_emptytile_bytes(self, tile):
        """
        Returns the 'empty tile' as raw PNG image data.
        """
        return self.get_emptytile(tile).read()
    
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import os

class FileSystemStorage(BaseStorage):
    """
    Storage backend that uses a directory to store actual image files. (Classic
    behavior of django-gheat.)
    """
    def __init__(self):
        self.storage_dir = settings.GHEAT_FILESYSTEM_STORAGE_DIR
        if not self.storage_dir:
            raise ImproperlyConfigured("The gheat FileSystem storage backend requires " + \
                "GHEAT_FILESYSTEM_STORAGE_DIR to be set.")
    
    def dir_for_tile(self, tile, mapname=""):
        """
        Returns the directory path that the given tile should be stored in.
        
        i.e. /tmp/gheat/defaultmap/firetrans/
        """
        return os.path.join(self.storage_dir, mapname, tile.color_scheme)
    
    def path_for_tile(self, tile, mapname=""):
        """
        Returns the path that should correspond to this tile file on the filesystem.
        """
        tiledir = self.dir_for_tile(tile, mapname)
        return os.path.join(tiledir, "%s-%s,%s.png" % (tile.zoom, tile.x, tile.y))
    
    def has_tile(self, tile, mapname=""):
        filepath = self.path_for_tile(tile, mapname)
        return os.path.exists(filepath)
        
    def get_tile(self, tile, mapname=""):
        # If the cache file for this tile does not exist
        if not self.has_tile(tile, mapname):
            # Generate the storage directory for this tile, if it doesn't exist
            tiledir = self.dir_for_tile(tile, mapname)
            if not os.path.exists(tiledir):
                os.makedirs(tiledir)
            
            # Generate the image
            fileobj = tile.generate()
            
            # Open the output file and write our data to it.
            tilepath = self.path_for_tile(tile, mapname)
            outfile = open(tilepath, 'wb')
            for line in fileobj:
                outfile.write(line)
            outfile.close()
            
            # Rewind our in-memory image pseudofile and return it
            fileobj.seek(0)
            return fileobj
        else:
            # Cache file exists, so return a file pointer to that
            tilepath = self.path_for_tile(tile, mapname)
            tilefile = open(tilepath, 'rb')
            return tilefile
    
    def get_emptytile(self, tile):
        storage_dir = os.path.join(self.storage_dir, "empty_tiles")
        empty_tile_path = os.path.join(storage_dir, "%s-empty.png" % tile.color_scheme)
        
        # If the empty tile for this scheme is not cached
        if not os.path.exists(empty_tile_path):
            # Generate the empty_tiles storage directory
            if not os.path.exists(storage_dir):
                os.makedirs(storage_dir)
            
            # Generate our empty tile
            fileobj = tile.get_empty()
            
            # Open the output file and write to it.
            outfile = open(empty_tile_path, 'wb')
            for line in fileobj:
                outfile.write(line)
            outfile.close()
            
            # Rewind our in-memory image pseudofile and return it
            fileobj.seek(0)
            return fileobj
        else:
            # Cache file exists, so return a file pointer to that
            tilefile = open(empty_tile_path, 'rb')
            return tilefile

class DjangoCacheStorage(BaseStorage):
    """
    Storage backend that stores binary image data in the cache backend defined in
    your Django project's settings.CACHE_BACKEND
    """
    pass

