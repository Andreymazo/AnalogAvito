from config.settings import ATTEMPTS
from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render, reverse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from ad.models import Category
from bulletin.serializers import (
    CategorySerializer,
    # CreateProfileSerializer,
    CustomUserLoginSerializer,
    OneTimeCodeSerializer,
    SignInSerializer,
    SignUpSerializer
)
from bulletin.utils import (
    check_ban,
    create_or_update_code,
    get_random_code,
    if_user_first
)
from users.models import (
    # COUNT_ATTEMPTS,
    # COUNT_SEND_CODE,
    CustomUser,
    OneTimeCode
)


TIME_OTC = 30 * 60  # Время жизни кода в секундах
# TIME_OTC = 5
# TIME_RESEND_CODE = 3 * 60  # Время между повторными отправками кода
TIME_RESEND_CODE = 10
COUNT_ATTEMPTS = 3
COUNT_SEND_CODE = 3


# def check_user_ban(user):
#     """Проверка бана пользователя."""
#     ban_time = check_ban(user)
#     if ban_time:
#         return Response(
#             {
#                 "message": "Вы забанены на 24 часа.",
#                 "ban_time": ban_time
#             },
#             status=status.HTTP_403_FORBIDDEN
#         )

# class CheckBanAttemptsMixin():
#     """Миксин для проверки бана пользователя и количества попыток."""

#     def check_user_ban(user):
#         """Проверка бана пользователя."""
#         ban_time = check_ban(user)
#         if ban_time:
#             return Response(
#                 {
#                     "message": "Вы забанены на 24 часа.",
#                     "ban_time": ban_time
#                 },
#                 status=status.HTTP_403_FORBIDDEN
#             )

#     def check_user_attempts(user):
#         """Проверка количества попыток ввода кода."""
#         otc = user.onetimecodes
#         if otc.count_attempts == 0:
#             user.is_banned = True
#             user.save()
#             return Response(
#                 {
#                     "message": (
#                         f"Вы ввели неправильно {COUNT_ATTEMPTS} раз. "
#                         "Вы забанены на 24 часа."
#                     ),
#                     "count_attempts": COUNT_ATTEMPTS
#                 },
#                 status=status.HTTP_403_FORBIDDEN
#             )


def home(request):
    context = {}
    return render(request, "bulletin/templates/bulletin/home.html", context)


class SignInView(APIView):
    """Вход пользователя."""

    def post(self, request):
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

        # try:
        #     otc = user.onetimecodes
        #     if otc.count_attempts == 0:
        #         # user.is_banned = True
        #         # user.save()
        #         return Response(
        #             {
        #                 "message": (
        #                     f"Вы ввели неправильно {COUNT_ATTEMPTS} раз. "
        #                     "Вы забанены на 24 часа."
        #                 ),
        #                 "count_attempts": COUNT_ATTEMPTS
        #             },
        #             status=status.HTTP_403_FORBIDDEN
        #         )
        # except OneTimeCode.DoesNotExist:
        #     pass

        # if not otc:
            # return Response(
            #     {"message": "Одноразовый код не найден."},
            #     status=status.HTTP_404_NOT_FOUND
            # )

        # CheckBanAttemptsMixin.check_user_ban(user)
        # CheckBanAttemptsMixin.check_user_attempts(user)

            # # Если пользователя нет, в ответе пишем, что не зарегистрирован
            # return Response(
            #     {
            #         "message": (
            #             "Пользователь с таким E-mail "
            #             "еще не зарегистрирован"
            #         )
            #     },
            #     status=status.HTTP_404_NOT_FOUND
            # )

        # ban_time = check_ban(user)
        # if ban_time:
        #     return Response(
        #         {
        #             "message": "Вы забанены на 24 часа.",
        #             "ban_time": ban_time
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        # if otc.count_attempts == 0:
        #         user.is_banned = True
        #         user.save()
        #         return Response(
        #             {"count_attempts": otc.count_attempts},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
                        # "message": (
                        #     f"Вы ввели неправильно {otc.count_attempts} раза "
                        #       "Вы забанены на 24 часа")

        
        # return redirect(reverse("bulletin:confirm_code"))


class ConfirmCodeView(APIView):
    """Подтверждение кода."""

    def post(self, request):
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

        # CheckBanAttemptsMixin.check_user_attempts(user)

        # if otc.count_attempts == 0:
        #     user.is_banned = True
        #     user.save()
        #     return Response(
        #         {
        #             "message": (
        #                 f"Вы ввели неправильно {COUNT_ATTEMPTS} раза. "
        #                 "Вы забанены на 24 часа."
        #             ),
        #             "remaining_attempts": otc.count_attempts
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        # if datetime.now(timezone.utc) - otc.created_at < timedelta(
        #         seconds=2
        #     ):#Проверяем, если свежий пользователь (изменения меньше 2х секунд, то есть только что создан код, то обнуляем попытки)
        #     print("datetime.now(timezone.utc) - otc.created_at", datetime.now(timezone.utc) - otc.created_at)
        #     otc.count_attempts = 0
        #     otc.save()
        serializer = OneTimeCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # otc.count_attempts = otc.count_attempts - 1
        # otc.save()

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
            if not user.is_first:
                login(request, user)
            otc.count_attempts = 0
            otc.count_send_code = COUNT_SEND_CODE
            otc.save(
                # update_fields=[
                #     "count_attempts",
                #     "count_send_code"
                # ]
            )

            serializer = SignInSerializer(user)
            return Response(
                # {"is_first": user.is_first},
                # {"user": user},  # Или сериализатор?
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

        serializer = SignUpSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.is_first = False
        user.save()
        login(request, user)
        # serializer = SignUpSerializer(user)
        return Response(
                # {"is_first": user.is_first},
                # {"user": user},  # Или сериализатор?
                serializer.data,
                status=status.HTTP_200_OK
            )


class NewCodeView(APIView):
    """Запрос на повторную отправку кода."""

    def post(self, request):
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

        # Проверяем бан пользователя
        ban_time = check_ban(user)
        if ban_time:
            return Response(
                {
                    "message": "Вы забанены на 24 часа.",
                    "ban_time": ban_time
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # if datetime.now(timezone.utc) - otc.updated_at > timedelta(
        #     seconds=TIME_OTC
        # ):
        #     if otc.count_send_code == COUNT_SEND_CODE:
        #         user.is_banned = True
        #         user. banned_at = datetime.now(timezone.utc)
        #         user.save()
        #         return Response(
        #             {
        #                 "message": ("Слишком много запросов на отправку кода. "
        #                             "Вы забанены на 24 часа.")
        #             },
        #             status=status.HTTP_403_FORBIDDEN
        #         )
        #     create_or_update_code(user)  # Повторная отправка кода
        #     otc.count_send_code += 1
        #     otc.save()

        #     return Response(
        #         {"message": "Время ожидания истекло."},
        #         status=status.HTTP_400_BAD_REQUEST
        #         )

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
        passed_time = (datetime.now(timezone.utc) - otc.updated_at)
        print(passed_time)
        formatted_time_resend_code = timedelta(seconds=TIME_RESEND_CODE)
        if passed_time < formatted_time_resend_code:
            left_resend_time = (
                formatted_time_resend_code - datetime.now(timezone.utc)
            )  # ДОДЕЛАТЬ!
            print(left_resend_time)
            return Response(
                {
                    "message": ("Между повторными отправками кода должно "
                                f"пройти {TIME_RESEND_CODE} секунд."),
                    "left_resend_time": left_resend_time
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
    """Выход из учетной записи пользователя."""
    logout(request)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


    # reffer = request.META.get("HTTP_REFERER")
    # if reffer:
    #     return redirect(reffer)
    # return redirect(reverse("bulletin:log_in"))

    # if user.onetimecodes:  # Обращаемся по обратному ключу onetimecodes, если код пользователя существует
    #     otc = OneTimeCode.objects.get(user=user)
    #     otc.code = code
    #     otc.remaining_attempts += 1
    #     otc.save(update_fields=["code", "remaining_attempts"])  # Поменяли только поле code, remaining_attempts
    # else:  # Polzovatel pervii raz zashel i u nego net coda
    #     otc = OneTimeCode.objects.create(user=user, remaining_attempts=0)  # создали новый код пользователя
    #     otc.save()
    # ------------------
    # code = get_random_code()
    # email = user.email
    # print(code)  # for test
    # # send_code_by_email(email, code)
    # otc, _ = OneTimeCode.objects.get_or_create(user=user)
    # otc.code = code
    # otc.save()

    # return otc

    # """Проверка наличия одноразового кода."""
    # try:
    #     otc = OneTimeCode.objects.get(user=user)
    # except OneTimeCode.DoesNotExist:
    #     otc = create_otc(user)
    # return otc


@api_view(["POST"])
def sign_up(request):
    """Регистрация пользователя."""
    if request.method == "POST":
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Если пользователя нет,то создаем его
            serializer.save(email=email)
        else:
            # Если пользователь есть, то в ответе это пишем
            return Response(
                {"error": "Пользователь с таким E-mail уже зарегистрирован"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем код для пользователя
        create_code(CustomUser.objects.get(email=email))
        request.session["email"] = email
        # check_ban(request)
        return Response(status=status.HTTP_200_OK) 
        # return redirect(reverse("bulletin:confirm_code"))
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
def create_profile(request):
    """Указать информацию о пользователе."""
    if request.method == "GET":
        serializer = CreateProfileSerializer()
        return Response({
            "data": serializer.data,
        })

    # Доработать: какие поля заполнять, какие обязательные
    if request.method == "POST":
        user = CustomUser.objects.get(email=request.session["email"])
        serializer = CreateProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save
        # login(request, user)
        # return redirect(reverse("bulletin:home"))

        code = get_random_code()
        # send_code_by_email(email, code)
        otc, _ = OneTimeCode.objects.get_or_create(user=user)
        otc.code = code
        otc.save()
        return Response(status=status.HTTP_200_OK) # Оставляем для фронта закомментированный код: куда что и с чем перенаправлять
        # return redirect(reverse(
        #     "bulletin:confirm_code",
        #     kwargs={
        #         "user_id": user.id,
        #     }
        # ))
    return Response(status=status.HTTP_200_OK)
    # return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def log_in(request):
    """Вход по одноразовому коду."""
    if request.method == "POST":
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Если пользователя нет, в ответе пишем, что не зарегистрирован
            return Response(
                {"error": ("Пользователь с таким E-mail "
                           "еще не зарегистрирован")},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, имеет ли пользователь бан.
        # Если возвращается пустая строка, т.е. false, то пишем, сколько времени еще бан будет
        # formatted_ban_time = check_ban(user)
        # if formatted_ban_time:
        #     return Response({
        #         "error": (f"Вы забанены на 24 часа. "
        #                   f"Осталось {formatted_ban_time}")
        #     })

        # create_code(user)
        # request.session["email"] = email

        # return redirect(reverse("bulletin:confirm_code"))

        # attempts_passed, attempts_left = check_remaining_attempts(user)

        # if attempts_left < 0:
        #     user.is_banned = True
        #     user.save()
        #     return Response({
        #         "error": (f"Вы ввели неправильно {attempts_passed} раза "
        #                   "Вы забанены на 24 часа")
        #     })

        formatted_ban_time = check_ban(user)
        if formatted_ban_time:
            return Response({
                "error": (f"Вы забанены на 24 часа. "
                          f"Осталось {formatted_ban_time}")
            })
        email_code = create_or_update_code(user)  # Либо создаем, либо меняем поле code в существующем коде пользователя и отправлям на confirm_code
        print("=========================email_code", email_code.code)
        request.session["email"] = email
        # request.session["email_code"] = email_code.code
        return Response(status=status.HTTP_200_OK) 
        # return redirect(reverse("bulletin:confirm_code"))
    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


# добавить permission, если забанен - доступа нет
@api_view(["POST"])
def confirm_code(request):
    """Подтверждение кода."""
    # print("request.session.get("email")", request.session.get("email"))
    if request.method == "POST":
       
        if request.session.get("email"):
            email = request.session["email"]
            user = CustomUser.objects.get(email=email)
        else:
            return redirect(reverse("bulletin:sign_up"))
        try:
            otc = OneTimeCode.objects.get(user_id=user.id)
        except OneTimeCode.DoesNotExist:
            return redirect(reverse("bulletin:log_in"))

           
            # print("email_code", otc)
        # else:
        #     return redirect(reverse("bulletin:sign_up"))
        # try:
        #     email = request.session["email"]
        #     user = CustomUser.objects.get(email=email)
        #     # email_code = request.session["email_code"]
        #     email_code = OneTimeCode.objects.get(user_id=user.id)
        #     print("email_code", email_code)
        # except email.DoesNotExist or email_code.DoesNotExist: # Прилетел как-то без емэйла и без кода, редиректим его обратно на логин
        #     return redirect(reverse("bulletin:log_in"))
        
        # user = CustomUser.objects.get(email=email)
        if not if_user_first(email) == True:# Если впервые зашел, перенаправим на регистрацию
            return Response(status=status.HTTP_200_OK) 
            # redirect(reverse("bulletin:sign_up"))

        formatted_ban_time = check_ban(user)
        if formatted_ban_time:
            return Response({
                "error": (f"Вы забанены на 24 часа. "
                          f"Осталось {formatted_ban_time}")
            })
        # otc = user.onetimecodes
        if otc.count_attempts > ATTEMPTS:
                user.is_banned = True
                user.save()
                return Response({
                    "error": (f"Вы ввели неправильно {otc.count_attempts} раза "
                              "Вы забанены на 24 часа")
                })
        if datetime.now(timezone.utc) - otc.created_at< timedelta(
                seconds=2
            ):#Проверяем, если свежий пользователь (изменения меньше 2х секунд, то есть только что создан код, то обнуляем попытки)
            print("datetime.now(timezone.utc) - otc.created_at", datetime.now(timezone.utc) - otc.created_at)
            otc.count_attempts = 0
            otc.save()
        serializer = OneTimeCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otc.count_attempts = otc.count_attempts + 1
            otc.save()
            email_code_value = serializer.validated_data["code"]
            # Проверяем срок действия кода, если просрочен, то отправляем снова
            if datetime.now(timezone.utc) - otc.updated_at > timedelta(
                seconds=TIME_OTC
            ):
                # otc.delete()
                print("if we hhere ??????????????")
                create_or_update_code(user)  # Повторная отправка кода? не лучше на log_in перенаправить? 
                
                return Response(
                    {"error": "Время ожидания истекло"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Если код подходит Проверяем пользователя:
            # если он впервые - отправляем заполнять данные, если нет - на главную
            if otc.code == email_code_value:
                print("777777777777777777")
                login(request, user)
                return redirect(reverse("bulletin:home"))

            return Response(
                {
                    "error": (f"Вы ввели код неправильно {otc.count_attempts} раза. "
                            )
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def get_new_code(request):
#     """Запросить новый код."""
#     email = request.session.get("email")
#     if email:
#         user = CustomUser.objects.get(email=email)
#         # if datetime.now(timezone.utc) - otc.updated_at > timedelta(
#         #     seconds=TIME_OTC
#         # ):
#         create_code(user)
#     # return redirect(reverse("bulletin:confirm_code"))


#         user.save()
#         login(request, user)
#         return Response(status=status.HTTP_200_OK) 
#         # return redirect("bulletin:home")
#     return Response(status=status.HTTP_200_OK)


# @api_view(["POST", "GET"])
# def log_out(request):
#     """Выход из учетной записи пользователя."""
#     logout(request)
#     reffer = request.META.get("HTTP_REFERER")
#     # if reffer:
#     #     return redirect(reffer)
#     # return redirect(reverse("bulletin:log_in"))
#     return Response(status=status.HTTP_200_OK) 
  
# @api_view(["POST"])
# def log_out(request):
#     """Выход из учетной записи пользователя."""
#     logout(request)
#     return Response(status=status.HTTP_200_OK)
#     # reffer = request.META.get("HTTP_REFERER")
#     # if reffer:
#     #     return redirect(reffer)
#     # return redirect(reverse("bulletin:log_in"))


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
