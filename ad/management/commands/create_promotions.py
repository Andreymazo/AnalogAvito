from django.core.management import BaseCommand
from ad.models import  Promotion
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATICFILES_DIRS, TEMPLATES
# from django.utils import timezone
from config import settings
from users.models import CustomUser, Profile
from datetime import datetime, time, timedelta, timezone
from django.contrib.contenttypes.models import ContentType
from ad.models import Car

def ff():


   time_paied_value1 =  datetime.now(timezone.utc) + timedelta(days=3) #make_aware(datetime.now()+ timedelta(days=3)).tzinfo 
   time_paied_value2 = datetime.now(timezone.utc) + timedelta(days=1)#make_aware(datetime.now() + timedelta(days=1)).tzinfo 
   time_paied_list = [time_paied_value1, time_paied_value2] #.strftime("%Y-%m-%d %H:%M:%S")
   car_inst1 = Car.objects.first()
   car_inst2 = Car.objects.last()
   isinstances_list = [car_inst1, car_inst2]
   
   for i, ii in zip(time_paied_list, isinstances_list):
        Promotion.objects.create(time_paied=i, content_type=ContentType.objects.get_for_model(ii), object_id=ii.id)

class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()