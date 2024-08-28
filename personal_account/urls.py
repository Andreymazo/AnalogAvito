from django.urls import path


from personal_account.apps import PersonalAccountConfig
from personal_account.views import UserBalanceAPIView, ChangeCurrencyApiView

app_name = PersonalAccountConfig.name

urlpatterns =[
    path('balance/', UserBalanceAPIView.as_view(), name='balance'),
    path('change-currency/', ChangeCurrencyApiView.as_view(), name='change_currency'),
]