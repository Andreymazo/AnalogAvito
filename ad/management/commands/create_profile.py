from django.core.management import BaseCommand
from users.models import CustomUser, Profile
from map.models import Marker
from django.contrib.gis.geos import Point
 
def ff():
    user_queryset = CustomUser.objects.all()

    user_list = [user_queryset.first(), user_queryset.last()]
    name_list = ["Kirill", "Serega"]
    phone_number_list = ["+7854328954", "+78095326765"]
    pnt2 = Marker.objects.first()
    pnt3 = Marker.objects.last()
    point_list = [pnt2, pnt3]
    for i, ii, iii, iiii in zip(user_list, name_list, phone_number_list, point_list):
        Profile.objects.create(user=i, name=ii, phone_number=iii, marker=iiii)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()