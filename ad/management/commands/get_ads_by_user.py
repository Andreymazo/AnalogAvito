import time
import requests
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
from django.apps import apps
from django.core.exceptions import FieldError


def ff():
    user = CustomUser.objects.get(email='asf1@adgf.fd')
    
    # print(user.profile.cars.all())

    conttype_queryset = ContentType.objects.all().filter()
    print('44444444444',ContentType.objects.get_for_model(user))
    app_models = apps.get_app_config('ad').get_models()
    for i in app_models:
        try:
            print('iiiiiiiiiiii', i)
            instance = i.objects.all().filter(profilee=user.profile)
            print('here smth', instance)
        except AttributeError as e:
            print(e)
        except FieldError as e:
            print(e)

    # print('conttype_queryset', conttype_queryset)
    # for i in app_models:
    #     print('222222222222', i)
    
    # for i in conttype_queryset:
    #     # print(i.model_class())
    #     try:
    #         instance = i.model_class().profilee.rel.model.objects.all().filter(profilee=user.profile)
    #         print('here smth', instance)
    #     except AttributeError as e:
    #         print(e)
        
   
class Command(BaseCommand):

    def add_arguments(self, parser):
        pass
    def handle(self, *args, **kwargs):
        ff()