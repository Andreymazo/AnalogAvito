from django.core.management import BaseCommand
from ad.models import Car, Like
from users.models import CustomUser, Profile
from django.contrib.contenttypes.models import ContentType


 
def ff():
    user_id = CustomUser.objects.get(id=14).id
    obj = Car.objects.get(pk=5)
    Like.objects.create(is_liked=False, user_id=user_id, content_type=ContentType.objects.get_for_model(obj), object_id=obj.id)
    #obj = self.model.objects.get(pk=pk)
#   content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()