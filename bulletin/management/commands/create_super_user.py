
from django.core.management import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):

        user = CustomUser.objects.create(username='andreymazo', email='andreymazoo@mail.ru', is_superuser=True, is_staff=True)
        user.set_password('qwert123asd')
        user.save()
#         {"username": "andreymazo@mail.ru",
# "password":"qwert123asd"}