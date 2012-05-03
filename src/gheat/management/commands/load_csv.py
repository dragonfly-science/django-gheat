import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection, transaction
from tempfile import TemporaryFile
from optparse import make_option


from gheat.default_settings import GHEAT_POINT_MODEL

# A bit of foo to dynamically import the Point class
module = '.'.join(GHEAT_POINT_MODEL.split('.')[:-1])
pointclass = GHEAT_POINT_MODEL.split('.')[-1]
Point = getattr(__import__(module, fromlist=[pointclass]), pointclass)

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import data from the csv file "filename", which has columns lat and long.'
    option_list = BaseCommand.option_list + (
        make_option('--lat',
            action = 'store',
            dest = 'lat',
            default = 'lat',
            help = 'Name of the latitude column'),
        make_option('--long',
            action = 'store',
            dest = 'long',
            default = 'long',
            help = 'Name of the longitude column'),
        make_option('--density',
            action = 'store',
            dest = 'density',
            default = 'density',
            help = 'Name of the longitude column'),
        )
    
    def handle(self, *args, **options):
        tempfile = TemporaryFile('w+r')
        reader = csv.DictReader(open(args[0]))
        for row in reader:
            lng = float(row[options['long']])
            lat = float(row[options['lat']])
            tempfile.write("%0.5f\t%0.5f\n" % (lng, lat))
        tempfile.seek(0)
        cursor = connection.cursor()
        cursor.execute('CREATE TEMPORARY TABLE _point_import (long FLOAT, lat FLOAT, density FLOAT);')
        cursor.copy_from(tempfile, '_point_import')
        cursor.execute("INSERT INTO %s (geometry) SELECT ST_SetSRID(ST_MakePoint(long, lat), 4326) AS geometry, density FROM _point_import;" % Point._meta.db_table)
        transaction.commit_unless_managed()

