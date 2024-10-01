
import os
from django.core.management import BaseCommand
from ad.models import IP, Advertisement, Car, Category
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATICFILES_DIRS, TEMPLATES
from config import settings
from users.models import CustomUser, Profile
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response

import re


def f(s):
    print('111',  s[1:])
    pattern = '^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-]*$'
    print(bool(re.search(r'^[0-9]*\Z', s[1:])))
    print(bool(re.match(pattern, s)))
       
    # car_instance=Car.objects.get(id=11)
    # profile_instance = Profile.objects.get(id=2)
    # print(car_instance.profilee.first())#andreymazoo@mail.ru
    # print(BASE_DIR)
    # user=CustomUser.objects.get(email="asf1@adgf.fd")
    # print("user.profile", user.profile.id)
    # try:
    #     ip_value = IP.objects.get_or_create(profile=user.profile)
    # except Profile.DoesNotExist:
    #     return Response({"message":"Profile doesn't exists. Create profile"}, status=status.HTTP_206_PARTIAL_CONTENT)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        f("+7981468659")

