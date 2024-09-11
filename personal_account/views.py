from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.apps import apps

from ad.models import Advertisement
from personal_account.models import Balance
from personal_account.serializers import BalanceSerializer, choose_serializer


@extend_schema(
    tags=["Аккаунт / Account"],
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
    tags=["Аккаунт / Account"],
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


@extend_schema(
    tags=["Аккаунт / Account"],
    description="Отображение активных объявлений пользователя в личном кабинете",
    summary="Активные объявления созданные пользователем",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Отображение активных объявлений",
            response=choose_serializer
        ),

    }
)
class GetCardsUserNotArchivedAPIList(ListAPIView):
    """Представление списка активных объявлений пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получение пользователя
        user = self.request.user

        # Фильтрация моделей по принадлежности только моделям наследованных от абстрактного класса Advertisement
        all_models = apps.get_app_config('ad').get_models()
        models = [model for model in all_models
                  if isinstance(model, ModelBase) and
                  issubclass(model, Advertisement)
                  ]

        # Получение типа профиля пользователя
        profile_content_type = ContentType.objects.get_for_model(user.profile.__class__)

        data = []

        for model in models:
            queryset = model.objects.all().filter(
                content_type=profile_content_type,
                object_id=user.profile.id,
                archived=False
            )

            serializer = choose_serializer(model.__name__)
            data.extend(serializer(queryset, many=True).data)

        return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Аккаунт / Account"],
    description="Отображение архивных объявлений пользователя в личном кабинете",
    summary="Объявления пользователя отправленные в архив",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Отображение архивных объявлений пользователя",
            response=choose_serializer
        ),

    }
)
class GetCardsUserArchivedAPIList(ListAPIView):
    """Представление списка архивных объявлений пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получение пользователя
        user = self.request.user

        # Фильтрация моделей по принадлежности только моделям наследованных от абстрактного класса Advertisement
        all_models = apps.get_app_config('ad').get_models()
        models = [model for model in all_models
                  if isinstance(model, ModelBase) and
                  issubclass(model, Advertisement)
                  ]

        # Получение типа профиля пользователя
        profile_content_type = ContentType.objects.get_for_model(user.profile.__class__)

        data = []

        for model in models:
            queryset = model.objects.all().filter(
                content_type=profile_content_type,
                object_id=user.profile.id,
                archived=True
            )

            serializer = choose_serializer(model.__name__)
            data.extend(serializer(queryset, many=True).data)

        return Response(data, status=status.HTTP_200_OK)


