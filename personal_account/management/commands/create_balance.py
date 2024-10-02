from django.core.management import BaseCommand
from users.models import CustomUser, Profile
from personal_account.models import Balance


def ff():
    
    obj1 = Profile.objects.first()
    obj2 = Profile.objects.last()
    obj_lst = [obj1, obj2]
    for i in obj_lst:
        Balance.create(profile=i, balance=1000)
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()