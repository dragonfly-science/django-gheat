import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection, transaction


from gheat.default_settings import GHEAT_POINT_MODEL

# A bit of foo to dynamically import the Point class
module = '.'.join(GHEAT_POINT_MODEL.split('.')[:-1])
pointclass = GHEAT_POINT_MODEL.split('.')[-1]
Point = getattr(__import__(module, fromlist=[pointclass]), pointclass)

class PointReader(object):
    def __init__(self, filename):
        self.fid = open(filename)
        self.reader = csv.DictReader(self.fid)
        self.count = 0

    def readline(self):
        try:
            row = self.reader.next()
            lat = float(row['lat'])
            lng = float(row['long'])
            text = "%0.5f\t%0.5f\n" % (lng, lat)
            self.count += 1
            print self.count, text[:-1]
            return text
        except StopIteration:
            return ''

    def read(self, n=-1):
        text = ''
        new = True
        while new and n > 0 and len(text) < n:
            new = self.readline()
            text += new
        if n >= 0 and len(text) > n:
            text = text[:n]
        return text

    def next():
        while True:
            new = self.readline()
            if new:
                return new
            else:
                raise StopIteration

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import data from the csv file "filename", which has columns lat and long.'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute('CREATE TEMPORARY TABLE _point_import (lat FLOAT, long FLOAT);')
        cursor.copy_from(PointReader(args[0]), '_point_import')
        cursor.execute("INSERT INTO %s (geometry) SELECT ST_SetSRID(ST_MakePoint(long, lat), 4326) AS geometry FROM _point_import;" % Point._meta.db_table)
        transaction.commit_unless_managed()

