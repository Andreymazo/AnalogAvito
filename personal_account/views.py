from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from personal_account.models import Balance
from personal_account.serializers import BalanceSerializer


class UserBalanceAPIView(RetrieveAPIView):
    """Эндпоинт для получения баланса и текущей валюты"""
    serializer_class = BalanceSerializer

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Вы не авторизованы"}, status=401)
        balance = Balance.objects.get(owner=request.user)
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)


class ChangeCurrencyApiView(APIView):
    """Представление для изменения валюты баланса пользователя."""

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return Response({"message": "Вы не авторизованы"}, status=401)

        balance = Balance.objects.get(owner=user)

        currency = {
            "RUB": "USD",
            "USD": "EUR",
            "EUR": "RUB",
        }

        balance.currency = currency.get(balance.currency, balance.currency)
        balance.save()
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)
