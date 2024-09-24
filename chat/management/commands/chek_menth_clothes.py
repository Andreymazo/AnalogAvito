from django.core.management import BaseCommand
from ad.models import Car, Category, Images, MenClothes
from map.models import Marker
from users.models import Profile
from django.contrib.contenttypes.models import ContentType
 
def ff():
    
    instance = MenClothes.objects.get(id=8)
    # print(instance.profilee.all().first().user.email)#__dict__)#(content_object=instance))#__dict__)#__dict__)#.user.email)
    print(instance.profilee.first())
    Profile
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()

    