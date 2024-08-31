from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from decimal import Decimal
from bulletin.serializers import SignUpSerializer
from personal_account.models import Balance
from users.models import CustomUser, OneTimeCode, Profile
from config import constants

class AuthApi(APITestCase):
    usd = Decimal(constants.USD)
    eur = Decimal(constants.EUR)

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email="andreymazo3@mail.ru")
    
    def test_balance_property_rub(self):
        balance_instance, _ = Balance.objects.get_or_create(balance=1000, currency="RUB", user=self.user)
        print(balance_instance, type(balance_instance))
        self.assertEqual(balance_instance.get_balance_in_currency,1000)
    
    def test_balance_property_usd(self):
        balance_instance, _ = Balance.objects.get_or_create(balance=1000, currency="USD", user=self.user)
        print('---------', self.usd)
        self.assertEqual(balance_instance.get_balance_in_currency,1000/self.usd)

    def test_balance_property_eur(self):
        balance_instance, _ = Balance.objects.get_or_create(balance=1000, currency="EUR", user=self.user)
        self.assertEqual(balance_instance.get_balance_in_currency,1000/self.eur)
