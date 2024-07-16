from django.core.management import BaseCommand
from users.models import CustomUser, Profile

 
def ff():
    user_queryset = CustomUser.objects.all()

    user_list = [user_queryset.first(), user_queryset.last()]
    name_list = ["Kirill", "Serega"]
    phone_number_list = ["+7854328954", "+78095326765"]

    for i, ii, iii in zip(user_list, name_list, phone_number_list):
        Profile.objects.create(user=i, name=ii, phone_number=iii)
  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()