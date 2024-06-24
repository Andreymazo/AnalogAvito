
from django.core.management import BaseCommand
from users.models import CustomUser
# from users.managers import CustomUserManager

class Command(BaseCommand):
    def handle(self, *args, **options):
        # create_superuser = CustomUserManager.create_superuser
        # user = CustomUser.objects.create_superuser( email = 'andreymazoo@mail.ru', password = 'qwert123asd', is_superuser=True, is_staff=True, is_active=True)
        # user.save()
        user = CustomUser.objects.create( email = 'andreymazoo@mail.ru', is_superuser=True, is_staff=True, is_active=True)#, password = 'qwert123asd'
        user.set_password('qwert123asd')
        user.save()
        
#         {"username": "andreymazo@mail.ru",
# "password":"qwert123asd"}