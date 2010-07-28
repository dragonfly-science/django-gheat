from django.contrib.gis.db import models

class FriendPoint(models.Model):
    """
        A simple representation of a point inside the gheat database
    """
    name = models.CharField(max_length=100)
    geometry = models.PointField()
    
    objects = models.GeoManager()
