from django.core.management import BaseCommand

from personal_account.models import Balance
from users.models import CustomUser
# from users.managers import CustomUserManager

class Command(BaseCommand):
    def handle(self, *args, **options):
        users_list_email = ["adsf@arfg.com", "lkgr@agr.agr", "asf1@adgf.fd"]
        users_lisy_passwords = ['qwert123asd', 'qwert123asd', 'qwert123asd']
        for i, ii in zip(users_list_email, users_lisy_passwords):
            user = CustomUser.objects.create( email = i,  password = ii, is_staff=True, is_active=False)
            # user.set_password('qwert123asd')
            user.save()
            # balance = Balance.objects.create(user=user)
            # balance.save()