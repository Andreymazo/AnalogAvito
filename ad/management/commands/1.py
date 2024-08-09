
from datetime import time
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

 #note settings is an object , hence you cannot import its contents

# settings.configure()

 #note LANGUAGES is a tuple of tuples



 #use lang_dict for your query.

# def token_verify(token):
#     return Token.objects.get(key=token).user

# car_instance = Car.objects.get(id=8)
    # f = ContentType.objects.get_for_model(type(car_instance))
    # print(f.id)

auth_url = "http://147.45.157.251:1554/api/v1/registration/"
registration_profile_url = "http://147.45.157.251:1554/api/v1/registration/profile/"
get_token_url = "http://147.45.157.251:1554/api/v1/auth/token/"
def ff(**kwargs):
    login = kwargs['login']
    password = kwargs['password']
    first_name = kwargs['first_name']
    last_name = kwargs['last_name']
    birthday = kwargs['birthday']
    phone = kwargs['phone']
    email = kwargs['email']
    
    data_auth_url = {"login": "androowefaevf", "password":"qwert123asd"}
    response = requests.post(auth_url, data_auth_url)
    print('step 1...', response.json())
    time.sleep(3)
    response = requests.post(get_token_url, data_auth_url)
    time.sleep(3)
    tokens = response.json()
    print('step 2....', tokens)
    header = tokens['access']
    print('header =======   ', header)
    # data_registration_profile = {"login": "aneymazooowefaevf", "password":"qwert123asd","first_name": "Andrey","last_name": "Mazo","birthday": "1999-01-11T00:00:00Z","phone": "77777771112","email": "andreymazo123@andrey.com"}
    data_registration_profile = {"login": login, "password":password,"first_name": first_name,"last_name": last_name,"birthday": birthday,"phone": phone,"email": email}
    response = requests.post(registration_profile_url, data_registration_profile, header=header)
    response('step 3...', response.json(), response.status_code)
    print('step 3...', response.json(), response.status_code)

    
    # response = requests.post(auth_url, data_registration_profile)
    
    print("response", response.json())#response {'login': ['user с таким login уже существует.']}#{'refresh': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMzIzMTUzMywiaWF0IjoxNzIzMTQ1MTMzLCJqdGkiOiI2MzQyODEzNjAwNDY0ZDY0YmEwMjhmNjVhNjEyYzU3YiIsInVzZXJfaWQiOjUsImF1ZCI6WyJleGFtcGxlLmNvbSIsIkVkdWNhdGlvbiIsIlFXRSFAMTIzIl0sImlzcyI6ImRldi5lY2EucnUifQ.Og-BIy3uh8aHjrww5lyBRoN-wK_JL6Zv7mJByfULVqeIieUsaZurJJGJ63tmT80547UQVrLo1DQBAB5l5qYjTNhFQOwkloMRym0CCmo13PFNW03-lNqp5BYlxk0iZe0lsTwlN8hgI-ugcUiIuEbFzmWvfq0AglN9Brx2TWjghfB1pIEaIu4rd33m38XbrX6BAE2GhtmQt6uMvfhNRLaA8M4or0W6B6HTKXHbNxYFlMY1OuxjbKcrd0jHKVvOGOjHqp-M4fGp-CPqsWQP7gv_qxiUdY7M95gsK1Zr05nOi3LUBfOjxCa9vHroCGzYZUfcTd-_SnZPxC5jsTKyNISfVg', 'access': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzMTQ2MDMzLCJpYXQiOjE3MjMxNDUxMzMsImp0aSI6IjBlZTBhM2I0MGI4ZjRiYmViYjIxYTA4YmViMzc1YzZmIiwidXNlcl9pZCI6NSwiYXVkIjpbImV4YW1wbGUuY29tIiwiRWR1Y2F0aW9uIiwiUVdFIUAxMjMiXSwiaXNzIjoiZGV2LmVjYS5ydSJ9.AqMLWYZmcPraVf5LNdQH3CVLS2gsJbq1SduueEDs4UJqxD_p2u0pMjUWcgyjvm8r4IikaxdOXH5jdB9TImNjFwJjsoxyBaQQc2JB81yLHJchF4onW8kP2pxitaXQ1gec0tXKLeWjgc1KMB8tXgfRm8Eo61CexucpPQvt-fVZcp-aEHoiTe8ep5af8YltEXJmV3apq2ZcX0TSgu370Z8Htk35EE1kl62s9lpp-0Lda9YKNmRI2DDtC0FmvuSJH7fOIxsJXWAMHuNVTrr7lEIGx_vfW9i4wcvikNjenmMsj0dCzy23VCCCc7dl4g1FDN54_XGiVnJ9yS36AE21XA8YyA'}

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('login', type=str, help='Указывает параметры пользователя')
        parser.add_argument('password', type=str, help='Указывает параметры пользователя')
        parser.add_argument('first_name', type=str, help='Указывает параметры пользователя')
        parser.add_argument('last_name', type=str, help='Указывает параметры пользователя')
        parser.add_argument('birthday', type=str, help='Указывает параметры пользователя')
        parser.add_argument('phone', type=str, help='Указывает параметры пользователя')
        parser.add_argument('email', type=str, help='Указывает параметры пользователя')
    def handle(self, *args, **kwargs):
        ff(**kwargs)

# РЕГИСТРАЦИЯ ЮЗЕРА: 
# http://147.45.157.251:1554/api/v1/registration/
# В теле запроса передавать login, password
# регистрация - статус 201

# ПОЛУЧЕНИЕ ТОКЕНОВ:
# api/v1/auth/token/
# В теле запроса передавать login, password
# возврат - пару токенов

# РЕГИСТРАЦИЯ ПРОФИЛЯ:
# api/v1/registration/profile/
# В запросе передавать:
# - заголовок авторизации с полученным токеном
# - тело запроса, пример:
# {
#  "id": 1,
#  "first_name": "qweqwe",
#  "last_name": "kmhjgkjmhg",
#  "birthday": "1999-01-11T00:00:00Z",
#  "phone": "787",
#  "email": "zxcxz44477@zxczxc.com"
# }

# ПОЛУЧЕНИЕ ПРОФИЛЯ:
# api/v1/profile/
# В запросе передавать заголовок заголовок авторизации с токеном 

# ОБНОВЛЕНИЕ ПРОФИЛЯ:
# /api/v1/auth/token/refresh/
# В теле запроса передавать токен обновления:
# {‘refresh’: ‘токен’}
# возврат - токен доступа

# ПРОВЕРКА ТОКЕНА:
# api/v1/auth/token/verify/
# В теле запроса передать проверяемый токен:
# {’token’: ‘проверяемый токен’}
# Возврат 200 если годен

# class Command(BaseCommand):
    # help = 'Создает случайных пользователей'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Указывает сколько пользователей необходимо создать')

    # def handle(self, *args, **kwargs):
    #     total = kwargs['total']
    #     for i in range(total):
            # User.objects.create_user(username=get_random_string(7), email='', password='1234567890')