from django.core.management import BaseCommand
from ad.models import Images
from users.models import Profile


 
def ff():
    """Создаем images"""
    profile_queryset = Profile.objects.all()
    profile1 = profile_queryset.last()
    profile2 = profile_queryset.first()
    profile_list = [profile1, profile2]
    images_list = ["/home/andrey_mazo/Pictures/Screenshots/22.png", "/home/andrey_mazo/Pictures/Screenshots/44.png"]
    for i,m in zip(profile_list, images_list):
        # card_instance, created = Images.objects.get_or_create(profile=i, content_object = i, image=m)
        image_instance = Images(content_object=i, image=m)
        image_instance.save()
        print(image_instance.content_object)
class Command(BaseCommand):
# kill -9 $(lsof -t -i:8000)
    def handle(self, *args, **options):
        ff()