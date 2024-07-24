from datetime import datetime, timedelta, timezone
from django.contrib.auth import login, logout
from django.core.signing import BadSignature, Signer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer
)
from rest_framework import permissions, serializers, status, viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from ad.models import Car, Category
from bulletin.serializers import (
    AlternativeAuthSerializer,
    CategorySerializer,
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
    check_email_phone,
    create_or_update_code,
)
from users.models import (
    CustomUser,
    OneTimeCode,
    Profile
)

  
"""Тренировочный ендпоинт для альтернативной авторизации"""
@api_view(["POST"])
def sign_in_alternative(request):
    if request.user.is_authenticated:
        logout(request)
        print('Разлогинили ...........')
    serializer = AlternativeAuthSerializer(data=request.data)
    if request.method=="POST":
        print('111111111111111111111s')
        if serializer.is_valid():
            print('request.user.is_authenticated____', request.user.is_authenticated)
            user_input_value = serializer.validated_data['user_input_value']
            user_input_value=check_email_phone(user_input_value)
            if user_input_value[1]=="email":
                user = CustomUser.objects.get(email=user_input_value[0])
                login(request, user)
                print('000_________request.user.is_authenticated____', request.user.is_authenticated)
            if user_input_value[1]=="phone":
                user = Profile.objects.get(phone_number=user_input_value[0]).user
                login(request, user)
            # print('user_input_value', user_input_value)
                print('request.user.is_authenticated____', request.user.is_authenticated)
            return Response(serializer.data)
        print('jjjjjjjjjjjjjj', serializer.data)
        return Response([serializer.errors, {"messg":"Invalid input"}])

        
    
class SignInView(APIView):
    """Вход пользователя."""

    @extend_schema(
        tags=["Вход/регистрация"],
        description="Аутентификация и создание пользователя.",
        summary="Вход пользователя",
        request=AlternativeAuthSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Успешная аутентификация",
                response=AlternativeAuthSerializer,
            ),
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Пользователь создан",
                response=AlternativeAuthSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Ошибка валидации, пользователь уже авторизован",
                response=inline_serializer(
                    name="ValidationErrorInSignIn",
                    fields={"email": serializers.ListField(
                        child=serializers.CharField()
                    )}
                    ),
                examples=[
                    OpenApiExample(
                        "Пользователь уже авторизован",
                        description=(
                            "Пример ответа, если пользователь "
                            "уже авторизирован"
                        ),
                        value={"message": "Вы уже авторизированы."},
                    ),
                    OpenApiExample(
                        "Ошибка валидации",
                        description=(
                            "Пример ответа при ошибке валидации поля email"
                        ),
                        value={"email": ["Сообщение об ошибке."]},
                    ),
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Пользователь забанен",
                response=inline_serializer(
                    name="UserBannedInSignIn",
                    fields={
                        "message": serializers.CharField(),
                        "ban_time": serializers.DateTimeField(),
                    }
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь забанен",
                        description=(
                            "Пример ответа, если пользователь забанен\n"
                            "\nban_time - время снятия бана"
                        ),
                        value={
                            "message": "Вы забанены на 24 часа.",
                            "ban_time": "2024-06-20T16:00:10Z"
                        },
                    ),
                ],
            )
        },
    )
    def post(self, request):
        # print('-------------------00---------------')
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )
        """Пробуем залогиниться по введенным данным"""
        serializer = AlternativeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_input_value = serializer.validated_data["user_input_value"]
        user_input_value = check_email_phone(user_input_value)
        
        if not user_input_value:# Сразу обезопасим себя от user_input_value=None
            return Response([serializer.data, {"message":"Ввели неправильные данные"}], status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        if user_input_value[1]=="email":
            try:
                email= user_input_value[0]      
                user = CustomUser.objects.get(email = email)
                """Сразу логинить нельзя, чел просто не будут вводить код, а пойдет на другие ендпоинты"""
                # print('ddd00000_________request.user.is_authenticated____', request.user.is_authenticated)
                # login(request, user=user)
                # print('dddd11111_________request.user.is_authenticated____', request.user.is_authenticated)
                return Response([serializer.data, {"message": "Авторизированы по емэйл"}])
            except CustomUser.DoesNotExist:
                user, is_created = CustomUser.objects.select_related(
                "onetimecodes"
                ).get_or_create(email=email)
        if user_input_value[1]=="phone":
            try:
                user = Profile.objects.get(phone_number=user_input_value[0]).user
                email = user.email
                """Сразу логинить нельзя, чел просто не будут вводить код, а пойдет на другие ендпоинты"""
                # print('000_________request.user.is_authenticated____', request.user.is_authenticated)
                # login(request, user=user)
                # print('001_________request.user.is_authenticated____', request.user.is_authenticated)
                return Response([serializer.data, {"message": "Авторизированы по телефону"}])
            except Profile.DoesNotExist:
                return Response([serializer.data, {"message":"Профиля с таким номером телефона не существует, введите свой емэйл или существующий номер телефона"}])
        # email = serializer.validated_data["email"]
        
        # user, is_created = CustomUser.objects.select_related(
        #         "onetimecodes"
        #     ).get_or_create(email=email)
        
        ban_time = check_ban(user)
        if ban_time:
            return Response(
                {
                    "message": "Вы забанены на 24 часа.",
                    "ban_time": ban_time
                },
                status=status.HTTP_403_FORBIDDEN
            )

        create_or_update_code(user)
        # request.session["email"] = email
        from django.core.signing import Signer
        signer = Signer()
        signed_value = signer.sign(email)

        response = (#Фронт попросил serializer.data тоже присылать
            Response(serializer.data, status=status.HTTP_201_CREATED)
            if is_created else
            Response(serializer.data, status=status.HTTP_200_OK)
        )
        response.set_cookie("email", signed_value, httponly=True)
        print("----------------111-------------------", response.cookies)
        print("---------------------222---------------", response.cookies["email"])
        return response


class ConfirmCodeView(APIView):
    """Подтверждение кода."""

    @extend_schema(
        tags=["Вход/регистрация"],
        description="Подтверждение кода.",
        summary="Подтверждение кода",
        request=OneTimeCodeSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Код подтвержден",
                # response=OneTimeCodeSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description=(
                    "Пользователь уже авторизован, неверная подпись cookie, "
                    "время ожидания истекло, неправильный ввод кода"
                ),
                response=inline_serializer(
                    name = "CustomUser",
                    fields = {"email":serializers.EmailField()}
                    # name="ValidationErrorInConfirmCode",
                    # fields={"email": serializers.ListField(
                    #     child=serializers.CharField()
                    # )}
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь уже авторизован",
                        description=(
                            "Пример ответа, если пользователь "
                            "уже авторизирован"
                        ),
                        value={"message": "Вы уже авторизированы."},
                    ),
                    OpenApiExample(
                        "Неверная подпись cookie",
                        description=(
                            "Пример ответа, если в cookie был изменен email "
                            "пользователя"
                        ),
                        value={"message": "Неверная подпись cookie."},
                    ),
                    OpenApiExample(
                        "Время ожидания истекло",
                        description=(
                            "Пример ответа, когда время жизни кода истекло"
                        ),
                        value={"message": "Время ожидания истекло."},
                    ),
                    OpenApiExample(
                        "Неправильный ввод одноразового кода",
                        description=(
                            "Пример ответа, когда пользователь ввел "
                            "код неправильно\n"
                            "\nremaining_attempts - количество попыток"
                        ),
                        value={
                            "message": ("Вы ввели код неправильно 2 раза."),
                            "remaining_attempts": 2
                        },
                    ),
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description=(
                    "Пользователь забанен, "
                    "превышен лимит попыток или запросов отправить код"
                ),
                response=inline_serializer(
                    name="UserBannedInConfirmCode",
                    fields={
                        "message": serializers.CharField(),
                        "ban_time": serializers.DateTimeField(),
                        "count_send_code": serializers.IntegerField(),
                        "remaining_attempts": serializers.IntegerField()
                    }
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь забанен",
                        description=(
                            "Пример ответа, если пользователь забанен\n"
                            "\nban_time - время снятия бана"
                        ),
                        value={
                            "message": "Вы забанены на 24 часа.",
                            "ban_time": "2024-06-20T16:00:10Z"
                        },
                    ),
                    OpenApiExample(
                        "Превышен лимит запросов кода",
                        description=(
                            "Пример ответа, когда количество запросов на "
                            "отправку кода превысило допустимое значение\n"
                            "\ncount_send_code - количество отправленных кодов"
                        ),
                        value={
                            "message": (
                                "Слишком много запросов на отправку кода. "
                                "Вы забанены на 24 часа."
                            ),
                            "count_send_code": 3
                        },
                    ),
                    OpenApiExample(
                        "Превышен лимит попыток ввода кода",
                        description=(
                            "Пример ответа, когда пользователь превысил "
                            "количество попыток неправильного ввода кода\n"
                            "\nremaining_attempts - количество попыток"
                        ),
                        value={
                            "message": (
                                "Вы ввели код неправильно 3 раза. "
                                "Вы забанены на 24 часа."
                            ),
                            "remaining_attempts": 3
                        },
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description=(
                    "Не найден пользователь, или одноразовый код, или "
                    "cookie с email"
                ),
                response=inline_serializer(
                    name="ObjectNotFoundInConfirmCode",
                    fields={"message": serializers.ListField(
                        child=serializers.CharField()
                    )}
                ),
            ),
        },
        parameters=[
            OpenApiParameter(
                name="Email",
                location=OpenApiParameter.COOKIE,
                description="Email пользователя",
                required=True,
                type=str
            ),
        ],
    )
    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # email = request.session.get("email")
        signer = Signer()
        try:
            signed_value = request.COOKIES.get("email")
            if signed_value:
                email = signer.unsign(signed_value)
            else:
                return Response(
                    {"message": "Cookie с email не найден."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except BadSignature:
            return Response(
                {"message": "Неверная подпись cookie."},
                status=status.HTTP_400_BAD_REQUEST
            )

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
                print("loged_in_________1___")
                login(request, user)
                print('request.user', request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            except Profile.DoesNotExist:
                pass
            print("not_loged_in______go_to_sign_up ______")
            otc.count_attempts = 0
            otc.count_send_code = 0
            otc.save()

            serializer = SignInSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_307_TEMPORARY_REDIRECT # Перенаправить на создание профиля
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

    @extend_schema(
        tags=["Вход/регистрация"],
        description="Ввод персональных данных пользователя.",
        summary="Регистрация пользователя",
        request=SignUpSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Успешный ввод персональных данных",
                response=SignUpSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description=(
                    "Пользователь уже авторизован, неверная подпись cookie"
                ),
                response=inline_serializer(
                    name="ValidationErrorInSignUp",
                    fields={
                        "name": serializers.ListField(
                            child=serializers.CharField()
                        ),
                        "phone_number": serializers.ListField(
                            child=serializers.CharField()
                        )
                    }
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь уже авторизован",
                        description=(
                            "Пример ответа, если пользователь "
                            "уже авторизирован"
                        ),
                        value={"message": "Вы уже авторизированы."},
                    ),
                    OpenApiExample(
                        "Неверная подпись cookie",
                        description=(
                            "Пример ответа, если в cookie был изменен email "
                            "пользователя"
                        ),
                        value={"message": "Неверная подпись cookie."},
                    ),
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description=("Пользователь забанен"),
                response=inline_serializer(
                    name="UserBannedInSignUp",
                    fields={
                        "message": serializers.CharField(),
                        "ban_time": serializers.DateTimeField(),
                    }
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь забанен",
                        description=(
                            "Пример ответа, если пользователь забанен\n"
                            "\nban_time - время снятия бана"
                        ),
                        value={
                            "message": "Вы забанены на 24 часа.",
                            "ban_time": "2024-06-20T16:00:10Z"
                        },
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description=("Не найден пользователь или cookie с email"),
                response=inline_serializer(
                    name="ObjectNotFoundInSignUp",
                    fields={"message": serializers.ListField(
                        child=serializers.CharField()
                    )}
                ),
            ),
        },
        parameters=[
            OpenApiParameter(
                name="Email",
                location=OpenApiParameter.COOKIE,
                description="Email пользователя",
                required=True,
                type=str
            ),
        ],
    )
    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # email = request.session.get("email")

        signer = Signer()
        try:
            signed_value = request.COOKIES.get("email")
            if signed_value:
                email = signer.unsign(signed_value)
            else:
                return Response(
                    {"message": "Cookie с email не найден."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except BadSignature:
            return Response(
                {"message": "Неверная подпись cookie."},
                status=status.HTTP_400_BAD_REQUEST
            )

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
        serializer.save()
        login(request, user)
        return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


class NewCodeView(APIView):
    """Запрос на повторную отправку кода."""

    @extend_schema(
        tags=["Вход/регистрация"],
        description="Запрос отправки кода на почту.",
        summary="Запрос кода",
        request=inline_serializer(
            name="NewCode",
            fields={}
        ),
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Код отправлен",
                response=inline_serializer(
                    name="CodeSent",
                    fields={"message": "Одноразовый код отправлен на почту."}
                ),
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description=(
                    "Пользователь уже авторизован, неверная подпись cookie, "
                    "не прошло достаточно времени между "
                    "повторными отправками одноразового кода"
                ),
                response=inline_serializer(
                    name="InvalidRequiest",
                    # fields={"message": "string"}
                    fields={
                        "message": serializers.CharField(),
                        "time": serializers.IntegerField(),
                        "next_send_time": serializers.DateTimeField()
                    }
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь уже авторизован",
                        description=(
                            "Пример ответа, если пользователь "
                            "уже авторизирован"
                        ),
                        value={"message": "Вы уже авторизированы."},
                    ),
                    OpenApiExample(
                        "Неверная подпись cookie",
                        description=(
                            "Пример ответа, если в cookie был изменен email "
                            "пользователя"
                        ),
                        value={"message": "Неверная подпись cookie."},
                    ),
                    OpenApiExample(
                        "Превышен лимит запросов кода",
                        description=(
                            "Пример ответа, когда между повторной отправкой "
                            "кода прошло недостаточно времени\n"
                            "\ntime - время таймаута между повторными "
                            "отправками кода в секундах\n"
                            "\nnext_send_time - время до следующей "
                            "отправки кода"
                        ),
                        value={
                            "message": (
                                "Между повторными отправками кода должно "
                                "пройти 100 секунд."
                            ),
                            "time": 180,
                            "next_send_time": "2024-06-20T16:00:10Z"
                        },
                    ),
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description=(
                    "Пользователь забанен или превышен лимит "
                    "попыток отправить код"
                ),
                response=inline_serializer(
                    name="UserBannedInNewCode",
                    fields={
                        "message": serializers.CharField(),
                        "ban_time": serializers.DateTimeField(),
                        "count_send_code": serializers.IntegerField()
                    }
                ),
                examples=[
                    OpenApiExample(
                        "Пользователь забанен",
                        description=(
                            "Пример ответа, если пользователь забанен\n"
                            "\nban_time - время снятия бана"
                        ),
                        value={
                            "message": "Вы забанены на 24 часа.",
                            "ban_time": "2024-06-20T16:00:10Z"
                        },
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description=(
                    "Не найден пользователь, или одноразовый код, или "
                    "cookie с email"
                ),
                response=inline_serializer(
                    name="ObjectNotFoundInNewCode",
                    fields={"message": serializers.ListField(
                        child=serializers.CharField()
                    )}
                ),
            ),
        },
        parameters=[
            OpenApiParameter(
                name="Email",
                location=OpenApiParameter.COOKIE,
                description="Email пользователя",
                required=True,
                type=str
            ),
        ],
    )
    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "Вы уже авторизированы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # email = request.session.get("email")

        signer = Signer()
        try:
            signed_value = request.COOKIES.get("email")
            if signed_value:
                email = signer.unsign(signed_value)
            else:
                return Response(
                    {"message": "Cookie с email не найден."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except BadSignature:
            return Response(
                {"message": "Неверная подпись cookie."},
                status=status.HTTP_400_BAD_REQUEST
            )

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

"""Здесь нет сериалайзера и сваггер ругается, нам вообще все эти апи здесь помоему не нужны"""
# @extend_schema(
#     tags=["Вход/регистрация"],
#     description="Разлогиниться.",
#     summary="Выйти",
#     request=inline_serializer(
#         name="LogOut",
#         fields={}
#     ),
#     responses={
#         status.HTTP_200_OK: OpenApiResponse(
#             description="Пользователь разлогинен",
#             # response=inline_serializer(
#             #     name="Пользователь разлогинен",
#             #     fields={"message": "Пользователь разлогинен."}
#             # ),
#         ),
#         status.HTTP_400_BAD_REQUEST: OpenApiResponse(
#             description=(
#                 "Пользователь уже авторизован"
#             ),
#             response=inline_serializer(
#                 name="InvalidRequest",
#                 fields={"message": serializers.CharField()}
#             ),
#             examples=[
#                 OpenApiExample(
#                     "Пользователь уже авторизован",
#                     description=(
#                         "Пример ответа, если пользователь "
#                         "уже авторизирован"
#                     ),
#                     value={"message": "Вы уже авторизированы."},
#                 ),
#             ],
#         ),
#     },
# )
# @api_view(["POST"])
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


# @api_view(["POST", "GET"])
# @permission_classes((permissions.IsAuthenticated,))
def verify_code(request):
    """Тестовая модель для проверки авторизации."""
    # print(request.session["email"])
    # print(request.session["code"])
    # return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для категорий."""
    http_method_names = ("get",)
    queryset = Category.objects.prefetch_related("children").all()
    serializer_class = CategorySerializer
