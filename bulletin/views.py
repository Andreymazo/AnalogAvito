from datetime import datetime, timedelta, timezone
from django.contrib.auth import login, logout
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from ad.models import Advertisement, Category
from bulletin.serializers import (
    AdvertisementSerializer,
    CategorySerializer,
    CustomUserLoginSerializer,
    OneTimeCodeSerializer,
    SignInSerializer,
    SignUpSerializer
)
from config.constants import (
    TIME_OTC,
    TIME_RESEND_CODE,
    COUNT_ATTEMPTS,
    COUNT_SEND_CODE
)
from bulletin.utils import (
    check_ban,
    create_or_update_code,
)
from users.models import (
    CustomUser,
    OneTimeCode,
    Profile
)


class SignInView(APIView):
    """Вход пользователя."""

    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = CustomUser.objects.select_related(
                "onetimecodes"  # Нужен?
            ).get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(email=email)

        ban_time = check_ban(user)
        if ban_time:
            return Response(
                {
                    "message": "Вы забанены на 24 часа.",
                    "ban_time": ban_time
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Либо создаем, либо меняем поле code в существующем коде пользователя
        # и отправлям на confirm_code
        create_or_update_code(user)
        request.session["email"] = email

        return Response(status=status.HTTP_200_OK)


class ConfirmCodeView(APIView):
    """Подтверждение кода."""

    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.session.get("email")
        try:
            user = CustomUser.objects.select_related(
                "onetimecodes"
            ).get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otc = user.onetimecodes
        except OneTimeCode.DoesNotExist:
            return Response(
                {"message": "Одноразовый код не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        ban_time = check_ban(user)
        if ban_time:
            return Response(
                {
                    "message": "Вы забанены на 24 часа.",
                    "ban_time": ban_time
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OneTimeCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_code = serializer.validated_data["code"]
        # Проверяем срок действия кода, если просрочен, то отправляем снова
        if datetime.now(timezone.utc) - otc.updated_at > timedelta(
            seconds=TIME_OTC
        ):
            if otc.count_send_code == COUNT_SEND_CODE:
                user.is_banned = True
                user. banned_at = datetime.now(timezone.utc)
                user.save()
                return Response(
                    {
                        "message": ("Слишком много запросов на отправку кода. "
                                    "Вы забанены на 24 часа."),
                        "count_send_code": otc.count_send_code
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            create_or_update_code(user)  # Повторная отправка кода
            otc.count_send_code += 1
            otc.save()

            return Response(
                {"message": "Время ожидания истекло."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otc.code == email_code:
            try:
                user.profile
                login(request, user)
            except Profile.DoesNotExist:
                pass
            otc.count_attempts = 0
            otc.count_send_code = 0
            otc.save()

            serializer = SignInSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        # otc.count_attempts = otc.count_attempts - 1
        otc.count_attempts += 1
        otc.save()
        # remaining_attempts - количество использованных попыток
        remaining_attempts = COUNT_ATTEMPTS - otc.count_attempts

        if otc.count_attempts == COUNT_ATTEMPTS:
            user.is_banned = True
            user.banned_at = datetime.now(timezone.utc)
            user.save(update_fields=["is_banned", "banned_at"])
            return Response(
                {
                    "message": ("Вы ввели код неправильно "
                                f"{otc.count_attempts} раза. "
                                "Вы забанены на 24 часа."),
                    "remaining_attempts": remaining_attempts
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {
                "message": (f"Вы ввели код неправильно "
                            f"{otc.count_attempts} раза."),
                "remaining_attempts": remaining_attempts
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUpView(APIView):
    """Регистрация пользователя."""

    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.session.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        ban_time = check_ban(user)
        if ban_time:
            return Response(
                {
                    "message": "Вы забанены на 24 часа.",
                    "ban_time": ban_time
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SignUpSerializer(
            data=request.data,
            context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        print('serializer.data',serializer.data)
        serializer.save()
        login(request, user)
        return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


class NewCodeView(APIView):
    """Запрос на повторную отправку кода."""

    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = request.session.get("email")
        try:
            user = CustomUser.objects.select_related(
                "onetimecodes"
            ).get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            otc = user.onetimecodes
        except OneTimeCode.DoesNotExist:
            return Response(
                {"message": "Одноразовый код не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        ban_time = check_ban(user)
        if ban_time:
            return Response(
                {
                    "message": "Вы забанены на 24 часа.",
                    "ban_time": ban_time
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Проверям количество уже отправленных кодов
        if otc.count_send_code == COUNT_SEND_CODE:
            user.is_banned = True
            user.save()
            return Response(
                {
                    "message": (
                        f"Вы запросили код более {COUNT_SEND_CODE} раз. "
                        "Вы забанены на 24 часа."
                    ),
                    "count_send_code": otc.count_send_code
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Проверяем, что между повторными отправками кода
        # было больше {TIME_RESEND_CODE} секунд
        # next_send_time - время до следующей отправки кода
        time_from_send = datetime.now(timezone.utc) - otc.updated_at
        if time_from_send < timedelta(seconds=TIME_RESEND_CODE):
            next_send_time = otc.updated_at + timedelta(
                seconds=TIME_RESEND_CODE
            )
            return Response(
                {
                    "message": ("Между повторными отправками кода должно "
                                f"пройти {TIME_RESEND_CODE} секунд."),
                    "time": TIME_RESEND_CODE,
                    "next_send_time": next_send_time
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        create_or_update_code(user)
        return Response(
            {"message": "Одноразовый код отправлен на почту."},
            status=status.HTTP_200_OK
        )


@api_view(["POST"])
def log_out(request):
    print(request.user.is_authenticated)
    """Выход из учетной записи пользователя."""
    if not request.user.is_authenticated:
        return Response(
            {"message": "Вы не авторизированы."},
            status=status.HTTP_400_BAD_REQUEST
        )

    logout(request)
    print(request.user.is_authenticated)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
@permission_classes((permissions.IsAuthenticated,))
def verify_code(request):
    """Тестовая модель для проверки авторизации."""
    # print(request.session["email"])
    # print(request.session["code"])
    # return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для категорий."""
    http_method_names = ("get", "post")
    queryset = Category.objects.prefetch_related('children').all()
    serializer_class = CategorySerializer


class AdvertisementList(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    name = "ad_list"
    filter_fields = ( 
        '-created', 
    )

    """Можно передать на фронт сразу все кверисеты, там делать видимым один и селектом(select) давать возможность 
    пользователю переключаться, тогда вся джанговская фильтрация не нужна"""
    
    # def get_queryset(self):
    #     queryset1 = Advertisement.objects.all()
    #     # queryset2 = Advertisement.objects.all()[:12]
    #     # queryset3 = Advertisement.objects.order_by('-created')
    #     # queryset = {"queryset1":queryset1, "queryset2":queryset2, "queryset3":queryset3}
    #     return queryset1.order_by('-created')
    """Кастомная пагинация на подружилась с фильтрацией"""
    # def get(self, request):
    #     paginator = PageNumberPagination()
    #     paginator.page_query_param = 'page'
    #     paginator.page_size_query_param = 'per_page'
    #     paginator.page_size = 1
    #     context = paginator.paginate_queryset(self.queryset, request)
    #     serializer1=AdvertisementSerializer(context, many=True)
    #     return paginator.get_paginated_response(serializer1.data)

