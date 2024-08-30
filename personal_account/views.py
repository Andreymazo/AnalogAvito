from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from personal_account.models import Balance
from personal_account.serializers import BalanceSerializer


@extend_schema(
    tags=["Кошелек/Wallet"],
    description="Отображение баланса и текущей валюты пользователя",
    summary="Баланс пользователя",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Отображение баланса и валюты",
            response=BalanceSerializer
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Пользователь не авторизован",
            response=(
                    {'message': 'Вы не авторизованы'}
            )
        )
    }
)
class UserBalanceAPIView(RetrieveAPIView):
    """Эндпоинт для получения баланса и текущей валюты"""
    serializer_class = BalanceSerializer

    def retrieve(self, request, *args, **kwargs):
        # проверяем прошел ли пользователь авторизацию
        if not request.user.is_authenticated:
            return Response({"message": "Вы не авторизованы"}, status=status.HTTP_401_UNAUTHORIZED)

        balance = Balance.objects.get(user=request.user)

        # Меняем баланс для отображения в соответствующей валюте, но НЕ записываем его в базу
        balance.balance = balance.get_balance_in_currency
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)


@extend_schema(
    tags=["Кошелек/Wallet"],
    description="Отображение баланса при изменении валюты",
    summary="Изменение валюты баланса",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Отображение баланса и измененной валюты",
            response=BalanceSerializer
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Пользователь не авторизован",
            response=(
                    {'message': 'Вы не авторизованы'}
            )
        )
    }
)
class ChangeCurrencyApiView(APIView):
    """Представление для изменения валюты баланса пользователя."""

    def get(self, request, *args, **kwargs):
        user = self.request.user
        # проверяем прошел ли пользователь авторизацию
        if not user.is_authenticated:
            return Response({"message": "Вы не авторизованы"}, status=status.HTTP_401_UNAUTHORIZED)

        balance = Balance.objects.get(user=user)

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
