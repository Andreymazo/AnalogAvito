# import datetime

from django.core.management import BaseCommand

from django.contrib.gis.geos import Point
from map.models import Marker


 
def ff():
    Marker.objects.create(name='1st', location=Point(50, 30))

class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()
