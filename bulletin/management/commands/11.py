
import os
from django.core.management import BaseCommand
from ad.models import IP, Advertisement, Category
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATICFILES_DIRS, TEMPLATES
# from django.conf import settings
from config import settings
from users.models import CustomUser, Profile
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
 #note settings is an object , hence you cannot import its contents

# settings.configure()

 #note LANGUAGES is a tuple of tuples



 #use lang_dict for your query.

# def token_verify(token):
#     return Token.objects.get(key=token).user
import re

    
def ff(s):
    pat_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    pat_phone = r"^(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
    if re.match(pat_email,s):
        print("Valid Email")
        return s
    if re.match(pat_phone, s):
        print('Valid phone')
        return s
    else:
        print("Invalid Email and Phone")
        return None
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff("+79219507388")

