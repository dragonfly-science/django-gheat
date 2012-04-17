import csv

from django.core.management.base import BaseCommand, CommandError
from gheat.models import Point

class Command(BaseCommand):
    args = '<filename>'
    help = 'Loads points from the csv file filename (with columns lat and lng)'

    def handle(self, *args, **options):
        filename = args[0]
        points = csv.DictReader(open(filename))
        for p in points:
            point = Point()
            point.latitude = p['lat']
            point.longitude = p['lng']
            point.density = 1
            point.save()
        
        
