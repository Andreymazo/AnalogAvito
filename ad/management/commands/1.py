
import os
from django.core.management import BaseCommand
from ad.models import IP, Advertisement
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATICFILES_DIRS, TEMPLATES
# from django.conf import settings
from config import settings
from users.models import CustomUser, Profile
from ad.models import Car
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.contenttypes.models import ContentType
 #note settings is an object , hence you cannot import its contents

# settings.configure()

 #note LANGUAGES is a tuple of tuples



 #use lang_dict for your query.

# def token_verify(token):
#     return Token.objects.get(key=token).user

def ff():
    """Принтим акцесс и рефреш токены"""
    car_instance = Car.objects.get(id=8)
    f = ContentType.objects.get_for_model(type(car_instance))
    print(f.id)

class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()