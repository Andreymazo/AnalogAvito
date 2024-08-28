from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from personal_account.models import Balance
from personal_account.serializers import BalanceSerializer


class UserBalanceAPIView(RetrieveAPIView):
    """Эндпоинт для получения баланса и текущей валюты"""
    serializer_class = BalanceSerializer

    def retrieve(self, request, *args, **kwargs):
        # проверяем прошел ли пользователь авторизацию
        if not request.user.is_authenticated:
            return Response({"message": "Вы не авторизованы"}, status=status.HTTP_401_UNAUTHORIZED)

        balance = Balance.objects.get(owner=request.user)

        # Меняем баланс для отображения в соответствующей валюте, но НЕ записываем его в базу
        balance.balance = balance.get_balance_in_currency
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)


class ChangeCurrencyApiView(APIView):
    """Представление для изменения валюты баланса пользователя."""

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # проверяем прошел ли пользователь авторизацию
        if not user.is_authenticated:
            return Response({"message": "Вы не авторизованы"}, status=status.HTTP_401_UNAUTHORIZED)

        balance = Balance.objects.get(owner=user)

        currency = {
            "RUB": "USD",
            "USD": "EUR",
            "EUR": "RUB",
        }

        balance.currency = currency.get(balance.currency, balance.currency)
        balance.save()

        # Меняем баланс для отображения в соответствующей валюте, но НЕ записываем его в базу
        balance.balance = balance.get_balance_in_currency
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)
