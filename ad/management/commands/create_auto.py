from django.core.management import BaseCommand
from ad.models import Car, Category, Images
from map.models import Marker
from users.models import Profile
from django.contrib.contenttypes.models import ContentType
 
def ff():
    
    profile_queryset = Profile.objects.all()
    profile1 = profile_queryset.first()
    profile2 = profile_queryset.last()
    # auto_list = [(), ()]
    profile_list = [profile1, profile2]
    mileage_list = [200000, 100000]
    transmission_list = ["AUTO", "MECHANICAL"]
    description_list = ["Very well car", "Much joy vehicle"]
    price_lst=[100000,30000]
    
    image_list = ["media/images/Screenshot_from_2024-07-22_12-52-04.png", "media/images/Screenshot_from_2024-07-24_10-28-11_cCIxuaC.png"]
    for i,m,t,d,z,zz in zip(profile_list, mileage_list, transmission_list, description_list, image_list, price_lst):
        
        car_inst = Car(content_object=i, mileage = m, transmission = t, description = d, price=zz, category = Category.objects.get(name="Автомобили"))
        car_inst.save()
        # car_inst = Car.objects.create(profile = i, mileage = m, transmission = t, description = d, category = Category.objects.get(name="Автомобили"))
        print("-------------------", ContentType.objects.get_for_model(car_inst))
        content_type = ContentType.objects.get_for_model(car_inst)
        Images.objects.create(image=z, content_type=content_type, object_id=car_inst.id)
    
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()