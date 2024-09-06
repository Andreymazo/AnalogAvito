
from django.core.management import BaseCommand
from users.models import CustomUser
from users.managers import CustomUserManager
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        user  = CustomUser(username="admin", email = 'andreymazoo@mail.ru', password = 'qwert123asd', \
                                    is_superuser=True, is_staff=True, is_active=True,)
        user.set_password('qwert123asd')
        # user.username='admin'
        user.save()
        
        {"username": "andreymazo@mail.ru",
"password":"qwert123asd"}
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDI2MzU4NCwiaWF0IjoxNzIwMTc3MTg0LCJqdGkiOiJiZWQzMTFkZWZjYWM0NzI4YmZkYWJlNTc5YjcyNDM3YyIsInVzZXJfaWQiOjMxfQ.QkVxDLetxmLMRMpXljU8A50U1hLFvI1eJML0HEA0gww",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMjYzNTg0LCJpYXQiOjE3MjAxNzcxODQsImp0aSI6IjI5NjFmOGQ2NmI1ZTQxMjc5NWJiMWEwMGRiMWI1ZDRmIiwidXNlcl9pZCI6MzF9.hgrFrpuR-ASyw5QwlyYXgWeQ4h70F26AxlQKF3-P7h8"
}