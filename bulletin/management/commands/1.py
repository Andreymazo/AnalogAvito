
import os
from django.core.management import BaseCommand
from ad.models import IP, Advertisement
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

def ff():
    """Принтим акцесс и рефреш токены"""
    user, _ = CustomUser.objects.get_or_create(email='andreymazo@mail.ru')
    refresh = RefreshToken.for_user(user)
    print('str(refresh.access_token: ', str(refresh.access_token))
    print('str(refresh): ', str(refresh))
    # return {
    #     'refresh': str(refresh),
    #     'access': str(refresh.access_token),
    # }
    """Выводим по токену юзера"""
    # token = AccessToken(refresh.access_token)
    token = AccessToken(str(refresh.access_token))
    user_id = token.payload['user_id']
    user = CustomUser.objects.get(id=user_id)
    print(user)


    # # ip_queryset = IP.objects.all()
    # # advert_list = [("ad1", "ad_disr_1", profile_queryset.get(id=5)), ("ad2","ad_disr_2", profile_queryset.get(id=6)), ("ad3","ad_disr_3", profile_queryset.get(id=6))]
    # ip_list = ["123", "234", "456"]
    # # for i in advert_list:
    # #     # print(i[0])
    # #     Advertisement.objects.create(title=i[0], description=i[1], profile=i[2])
    # # print(Advertisement.objects.all().values_list('profile_id'))
    # advertizement_queryset = Advertisement.objects.all()
    # print(Advertisement.objects.all())
    # print(BASE_DIR)
    # for i, j, ii in zip(ip_list, profile_queryset, advertizement_queryset):
    #     IP.objects.create(ip=i, profile=j, advertisement=ii)
    #########################
    # advertisement = advertizement_queryset.get(id=50)
    # profile = profile_queryset.get(id=5) 
    # IP.objects.create(ip="123", profile=profile, advertisement=advertisement)
    # user = CustomUser.objects.get(email='andreymazo@mail.ru')
    # otc = user.onetimecodes
    # print(otc)
    # DJANGO_SETTINGS_MODULE=settings
    # print(os.environ['DJANGO_SETTINGS_MODULE'])
    # lang_dict = dict(settings.LANGUAGES)
    # user = CustomUser.objects.all().get(pk=17)
    # print(CodeCustomuser.objects.filter(customuser_id=user.id).exists())
    # code_user = user.codecustomuser.name
    # print (lang_dict)
    # print(BASE_DIR)
    # print(STATIC_URL, "00000", STATICFILES_DIRS)
    # print(TEMPLATES[0].get('DIRS'))
    
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()

