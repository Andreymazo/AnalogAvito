from django.urls import path

from personal_account.apps import PersonalAccountConfig
from personal_account.views import UserBalanceAPIView, ChangeCurrencyApiView, GetCardsUserNotArchivedAPIList, \
    GetCardsUserArchivedAPIList

app_name = PersonalAccountConfig.name

urlpatterns = [
    path('balance/', UserBalanceAPIView.as_view(), name='balance'),
    path('change-currency/', ChangeCurrencyApiView.as_view(), name='change_currency'),
    path('cards/', GetCardsUserNotArchivedAPIList.as_view(), name='cards'),
    path('archived/', GetCardsUserArchivedAPIList.as_view(), name='archived'),
]
