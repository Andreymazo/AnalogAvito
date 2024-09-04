from django.core.management import BaseCommand
from ad.models import Car, Favorite
from users.models import CustomUser
from django.contrib.contenttypes.models import ContentType


 
def ff():
    user_id = CustomUser.objects.first().id
    obj = Car.objects.first()
    fav_instance = Favorite(is_favorited=False, content_object=obj)#content_type=ContentType.objects.get_for_model(obj), object_id=obj.id)
    fav_instance.save()
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()