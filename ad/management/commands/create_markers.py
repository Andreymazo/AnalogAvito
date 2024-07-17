from django.contrib.gis.db.models import PointField

from django.core.management import BaseCommand

from django.contrib.gis.geos import Point

from map.models import Marker
 

def ff():
    pnt1 = Point(5, 23)
    pnt2 = Point(30, 60)
    pnt3 = Point(35, 55)
    point_list = [pnt1, pnt2, pnt3]
    name_list = ["Point1", "Point2", "Point3"]

    for i,ii in zip(name_list, point_list):
        Marker.objects.create( name=i, location=ii)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()