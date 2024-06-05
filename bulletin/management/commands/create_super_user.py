from django.core.management import BaseCommand

from catalog.models import CustomUser


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        # user = CustomUser.objects.create(
        #     email='andreymazo@mail.ru',
        #     is_admin=True,
        #     is_staff=True,
        #     banned = False,
        # )
        # # user.set_password('qwert123asd')#{"token":"ec700f613de4a2bf4967785b415878390eb33ea2"}
        # user.is_superuser = True
        # user.save()

        user = CustomUser.objects.get(id=15)
        user.codes_inputs=0
        user.save()
#         {"username": "andreymazo@mail.ru",
# "password":"qwert123asd"}
