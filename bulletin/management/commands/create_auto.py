from django.core.management import BaseCommand
from ad.models import Car, Category
from map.models import Marker
from users.models import Profile

 
def ff():
    
    profile_queryset = Profile.objects.all()
    profile1 = profile_queryset.first()
    profile2 = profile_queryset.last()
    # auto_list = [(), ()]
    profile_list = [profile1, profile2]
    mileage_list = [200000, 100000]
    transmission_list = ["AUTO", "MECHANICAL"]
    description_list = ["Very well car", "Much joy vehicle"]
    marker_queryset = Marker.objects.all()
    marker_list = [marker_queryset.first(), marker_queryset.last()]
    for i,m,t,d,v in zip(profile_list, mileage_list, transmission_list, description_list, marker_list):
        Car.objects.create(profile = i, mileage = m, transmission = t, description = d, category = Category.objects.get(name="Транспорт"), marker=v)
    
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()