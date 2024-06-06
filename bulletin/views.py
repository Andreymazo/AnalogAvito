from datetime import datetime, timedelta, timezone

# from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render, reverse
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from bulletin.serializers import (CustomUserLoginSerializer,
                                  OneTimeCodeSerializer,
                                  PersonalInfoSerializer)
from bulletin.utils import create_otc, get_random_code, send_code_by_email
from users.models import CustomUser, OneTimeCode

TIME_BAN = 24 * 60 * 60
TIME_OTC = 30 * 60


def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)


# @api_view(["POST", "GET"])
# def log_in(request):
#     """Вход по одноразовому коду."""
#     if request.method == "POST":
#         serializer = CustomUserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         email = serializer.validated_data["email"]
#         request.session["email"] = email

#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             user = CustomUser.objects.create(username=email, email=email)

#         if user.is_banned:
#             ban_time = datetime.now(timezone.utc) - user.banned_at
#             if ban_time < timedelta(seconds=TIME_BAN):
#                 hours, minutes = str(ban_time).split(":")[:2]
#                 return Response(
#                     {"error": f"Вы забанены на 24 часа. "
#                      f"Осталось: {hours} часов {minutes} минут."}
#                 )

#             user.is_banned = False
#             user.save()
#             print(f"Пользователь {user} разбанен по истечении времени.")  # for test

#         code = get_random_code()
#         print(code)  # for test
#         # send_code_by_email(email, code)
#         otc, _ = OneTimeCode.objects.get_or_create(user=user)
#         otc.code = code
#         otc.save()
#         print("Перенаправление на подтверждение кода.")  # for test
#         return redirect(reverse(
#             "bulletin:confirm_code"
#             # kwargs={
#             #     "user_id": user.id,
#             # }
#         ))

#     serializer = CustomUserLoginSerializer()
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["POST", "GET"])
# def confirm_code(request, **kwargs):
#     """Подтверждение кода."""
#     email = request.session["email"]
#     print(email)
#     # user_id = kwargs["user_id"]
#     serializer = OneTimeCodeSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email_code = serializer.validated_data["code"]
#     print(email_code)

#     user = CustomUser.objects.filter(id=user_id).first()
#     otc = OneTimeCode.objects.filter(user=user).first()

#     if datetime.now(timezone.utc) - otc.updated_at > timedelta(
#         seconds=TIME_OTC
#     ):
#         otc.delete()
#         return Response(
#             {"error": "Срок действия одноразового кода истек."},
#             status=status.HTTP_400_BAD_REQUEST
#         )  # Добавить повторную отправку кода.

#     if otc.code == email_code:
#         otc.delete()
#         if user.is_first:
#             return redirect(reverse(
#                 "bulletin:sign_up",
#                 kwargs={"user_id": user_id}
#             ))

#         login(request, user)
#         return redirect("bulletin:home")

#     if otc.remaining_attempts != 1:
#         otc.remaining_attempts -= 1
#         otc.save()
#         return Response(
#             {
#                 "error": ("Неверный код, повторите попытку. "
#                           f"Осталось: {otc.remaining_attempts}.")
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     user.banned_at = datetime.now(timezone.utc)
#     user.is_banned = True
#     user.save()

#     return Response(
#         {"error": "Вы забанены на 24 часа за 3 неудачные попытки ввода кода."},
#         status=status.HTTP_400_BAD_REQUEST
#     )


@api_view(["POST"])
def sign_up(request):
    """Регистрация пользователя."""
    # if request.method == "POST":
    serializer = CustomUserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]

    try:
        CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        serializer.save(username=email)
    else:
        return Response(
            {"error": "Пользователь с таким E-mail уже зарегистрирован"},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.session["email"] = email
    return redirect(reverse("bulletin:confirm_code"))

    # serializer = CustomUserLoginSerializer()
    # return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def log_in(request):
    """Вход по одноразовому коду."""
    serializer = CustomUserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]

    try:
        CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Пользователь с таким E-mail еще не зарегистрирован"},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.session["email"] = email
    return redirect(reverse("bulletin:confirm_code"))


@api_view(["POST"])
def confirm_code(request):
    """Подтверждение кода."""
    email = request.session["email"]
    print(email)  # for test
    user = CustomUser.objects.get(email=email)

    if user.is_banned:
        ban_time = datetime.now(timezone.utc) - user.banned_at
        if ban_time < timedelta(seconds=TIME_BAN):
            formatted_ban_time = ":".join(str(ban_time).split(":")[:2])
            return Response(
                {"error": (f"Вы забанены на 24 часа. "
                           f"Осталось {formatted_ban_time}")}
            )

        user.is_banned = False
        user.save()
        print(f"Пользователь {user} разбанен по истечении времени.")  # for test

    try:
        otc = OneTimeCode.objects.get(user=user)
    except OneTimeCode.DoesNotExist:
        otc = create_otc(user)

# if request.method == "POST":
    serializer = OneTimeCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email_code = serializer.validated_data["code"]
    print(email_code)

    if datetime.now(timezone.utc) - otc.updated_at > timedelta(
        seconds=TIME_OTC
    ):
        otc.delete()
        create_otc(user)  # Повторная отправка кода?
        return Response(
            {"error": "Время ожидания истекло"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if otc.code == email_code:
        otc.delete()
        login(request, user)
        # reffer = request.META.get("HTTP_REFERER")
        # if reffer:
        #     return redirect(reffer) -------- перенаправляет не так, как надо
        return redirect(reverse("bulletin:home"))

    if otc.remaining_attempts != 1:
        otc.remaining_attempts -= 1
        otc.save()
        return Response(
            {"error": "Неверный код"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.banned_at = datetime.now(timezone.utc)
    user.is_banned = True
    user.save()

    return Response(
        {
            "error": ("Вы забанены на 24 часа за "
                      "3 неудачные попытки ввода кода")
            },
        status=status.HTTP_400_BAD_REQUEST
    )

    # serializer = OneTimeCodeSerializer(data=request.data)
    # return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["POST", "GET"])
# def sign_up(request, **kwargs):
#     """Ввод персональных данных."""
#     serializer = PersonalInfoSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user_id = kwargs["user_id"]
#     user = CustomUser.objects.filter(id=user_id).first()

#     if request.method == "POST":
#         user.username = serializer.validated_data["username"]  # Обязательное?
#         # user.phone_number = serializer.validated_data["phone_number"]
#         user.first_name = serializer.validated_data.get("first_name", "")
#         user.last_name = serializer.validated_data.get("last_name", "")
#         user.info = serializer.validated_data.get("info", "")
#         user.is_first = False
#         user.save()

#         login(request, user)

#         reffer = request.META.get("HTTP_REFERER")
#         if reffer:
#             return redirect(reffer)
#         return redirect(reverse("bulletin:home"))
#         # return redirect("bulletin:home")
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_new_code(request):
    """Запросить новый код."""
    email = request.session.get("email")
    if email:
        user = CustomUser.objects.get(email=email)
        # if datetime.now(timezone.utc) - otc.updated_at > timedelta(
        #     seconds=TIME_OTC
        # ):
        create_otc(user)
    return redirect(reverse("bulletin:confirm_code"))


@api_view(["POST"])
def log_out(request):
    """Выход из учетной записи пользователя."""
    logout(request)
    return Response(status=status.HTTP_200_OK)
    # reffer = request.META.get("HTTP_REFERER")
    # if reffer:
    #     return redirect(reffer)
    # return redirect(reverse("bulletin:log_in"))


@api_view(["POST", "GET"])
@permission_classes((permissions.IsAuthenticated,))
def verify_code(request):
    """Тестовая модель для проверки авторизации."""
    # print(request.session["email"])
    # print(request.session["code"])
    # return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
