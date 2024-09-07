from django.core.management import BaseCommand
from users.models import CustomUser, Profile
from map.models import Marker
from django.contrib.gis.geos import Point
 
def ff():
    user_queryset = CustomUser.objects.all()

    # user_list = [user_queryset.first(), user_queryset.last()]
    user_list = [user for user in user_queryset]
    name_list = ["Kirill", "Serega", "Max", "Sasha"]
    phone_number_list = ["+7854328954", "+78095326765", "+7897234980", "+798345975"]
    pnt2 =Point(23, 55)
    pnt3 = Point(25, 56)
    point_list = [pnt2, pnt3]
    for i, ii, iii in zip(user_list, name_list, phone_number_list):
        profile = Profile(user=i, name=ii, phone_number=iii, content_object=i)
        profile.save()
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()