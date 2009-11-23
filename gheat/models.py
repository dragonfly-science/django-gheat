from django.contrib.gis.db import models

# Create your models here.
class Point(models.Model):
    """
        A simple representation of a point inside the gheat database
    """
    uid = models.CharField(max_length=100, name='unique identifier')
    geometry = models.PointField()
    modtime = models.DateTimeField(auto_now = True,
        name='Last modification time', null=True)
    density = models.PositiveIntegerField(default=0, editable=False,
        name='density of the current point')

    objects = models.GeoManager()

    class Meta:
        unique_together = ('uid',)
