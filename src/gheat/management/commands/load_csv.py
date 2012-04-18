import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection


from gheat.default_settings import GHEAT_POINT_MODEL

# A bit of foo to dynamically import the Point class
module = '.'.join(GHEAT_POINT_MODEL.split('.')[:-1])
pointclass = GHEAT_POINT_MODEL.split('.')[-1]
Point = getattr(__import__(module, fromlist=[pointclass]), pointclass)

class PointReader(object):
    def __init__(self, filename):
        self.fid = open(filename)
        self.reader = csv.DictReader(self.fid)

    def readline(self):
        row = self.reader.next()
        geometry = "ST_GeomFromText('POINT(%(long)s %(lat)s)')" % row
        return geometry

    def read(self, n=-1):
        text = self.readline()
        while n <= 0 or len(text) < n:
            text += '\n'
            try:
                text += self.readline()
            except:
                break
        if n > 0 and len(text) < n:
            text = text[:n]
        return text

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import data from the csv file "filename", which has columns lat and long.'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.copy_from(PointReader(args[0]), Point._meta.db_table, columns=('geometry',))


