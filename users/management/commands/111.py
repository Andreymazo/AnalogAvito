
import os
from django.core.management import BaseCommand
from ad.models import IP, Advertisement, Category
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATICFILES_DIRS, TEMPLATES
from config import settings
from users.models import CustomUser, Profile
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response

import re


def f():
    print(BASE_DIR)
    user=CustomUser.objects.get(email="asf1@adgf.fd")
    print("user.profile", user.profile.id)
    # try:
    #     ip_value = IP.objects.get_or_create(profile=user.profile)
    # except Profile.DoesNotExist:
    #     return Response({"message":"Profile doesn't exists. Create profile"}, status=status.HTTP_206_PARTIAL_CONTENT)

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        f()

