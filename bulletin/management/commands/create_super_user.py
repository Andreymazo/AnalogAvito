
from django.core.management import BaseCommand
from users.models import CustomUser
from users.managers import CustomUserManager
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        ct = ContentType.objects.get(model='customuser')
        ct_class = ct.model_class()
        ct_instance = ct_class()
        ct_instance.username = "admin"
        ct_instance.email = 'andreymazoo@mail.ru'
        ct_instance.password = 'qwert123asd'
        ct_instance.object_id = ct_class.id
        ct_instance.save()

        # user_type = ContentType.objects.get(app_label = "users", model = "customuser")
        # user_model_class = user_type.model_class()
        # specific_user = user_type.get_object_for_this_type(username = 'Guido')
        # content_type = ContentType.objects.get_for_model(CustomUser)
        # user  = CustomUser(username="admin", email = 'andreymazoo@mail.ru', password = 'qwert123asd', \
        #                             is_superuser=True, is_staff=True, is_active=True, content_type=content_type, object_id = ct_instance.id())
        # user.set_password('qwert123asd')
        # # user.username='admin'
        # user.save()
        
#         {"username": "andreymazo@mail.ru",
# "password":"qwert123asd"}
# {
#   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMDI2MzU4NCwiaWF0IjoxNzIwMTc3MTg0LCJqdGkiOiJiZWQzMTFkZWZjYWM0NzI4YmZkYWJlNTc5YjcyNDM3YyIsInVzZXJfaWQiOjMxfQ.QkVxDLetxmLMRMpXljU8A50U1hLFvI1eJML0HEA0gww",
#   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMjYzNTg0LCJpYXQiOjE3MjAxNzcxODQsImp0aSI6IjI5NjFmOGQ2NmI1ZTQxMjc5NWJiMWEwMGRiMWI1ZDRmIiwidXNlcl9pZCI6MzF9.hgrFrpuR-ASyw5QwlyYXgWeQ4h70F26AxlQKF3-P7h8"
# }