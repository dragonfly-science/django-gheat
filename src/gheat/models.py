from django.contrib.gis.db import models

class Point(models.Model):
    """
        A simple representation of a point inside the gheat database
    """
    geometry = models.PointField() 
    density = models.FloatField(default=1.0) 
    objects = models.GeoManager()
