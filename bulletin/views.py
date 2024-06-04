from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render, reverse
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from bulletin.serializers import (LoginSerializer, OneTimeCodeSerializer,
                                  PersonalInfoSerializer)
from bulletin.utils import get_random_code, send_code_by_email
from users.models import CustomUser, OneTimeCode


TIME_BAN = 24 * 60 * 60


def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)


@api_view(["POST", "GET"])
def login_view(request):
    """Вход по одноразовому коду."""
    # if request.method == 'GET':
    #         serializer = LoginSerializer()
    #         return Response({
    #            'data':serializer.data,
    #          })
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if request.method == "POST":
        email = serializer.validated_data["email"]

        # print(f"HTTP_COOKIE: {request.META.get("HTTP_COOKIE")}")
        # print(f"CSRF_COOKIE: {request.META.get("CSRF_COOKIE")}")
        # print(f"COOKIES: {request.COOKIES}")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(username=email, email=email)

        # if user.is_banned:
        #     ban_time = datetime.now(timezone.utc) - user.banned_at
        #     if ban_time < timedelta(seconds=TIME_BAN):
        #         return Response(
        #             {"error": ("Вы забанены на 24 часа. "
        #                        f"Осталось: {ban_time}.")}
        #         )

        #     user.is_banned = False
        #     user.save()

        code = get_random_code()
        # send_code_by_email(email, code)
        otc, _ = OneTimeCode.objects.get_or_create(user=user)
        otc.code = code
        otc.save()

        return redirect(reverse(
            "bulletin:confirm_code",
            kwargs={
                "user_id": user.id,
            }
        ))
    return Response(status=status.HTTP_400_BAD_REQUEST)
    # return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
def confirm_code(request, **kwargs):
    """Подтверждение кода."""
    user_id = kwargs["user_id"]
    serializer = OneTimeCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email_code = serializer.validated_data["code"]
    print(email_code)

    user = CustomUser.objects.filter(id=user_id).first()
    otc = OneTimeCode.objects.filter(user=user).first()

    # print(otc.updated_at)
    # print(datetime.now())
    # print(datetime.now(timezone.utc))
    # print(timedelta(seconds=settings.OTC_TIME))
    # timedelta(0, settings.OTC_TIME, 0)
    if datetime.now(timezone.utc) - otc.updated_at > timedelta(seconds=settings.OTC_TIME):
        otc.delete()
        return Response(
            {"error": "Срок действия одноразового кода истек."},
            status=status.HTTP_400_BAD_REQUEST
        )  # Добавить повторную отправку кода.

    if otc.code == email_code:
        otc.delete()
        if user.is_first:
            return redirect(reverse(
                "bulletin:personal_info",
                kwargs={"user_id": user_id}
            ))

        login(request, user)
        return redirect("bulletin:home")

    if otc.remaining_attempts != 0:
        otc.remaining_attempts -= 1
        otc.save()
        return Response(
            {
                "error": ("Неверный код, повторите попытку. "
                          f"Осталось: {otc.remaining_attempts}.")
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # user.banned_at = datetime.now(timezone.utc)
    # user.save()
# Иначе бан на 24 часа сделать
    return Response(
        {"error": "Вы забанены на 24 часа за 3 неудачные попытки ввода кода."},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST", "GET"])
def personal_info(request, **kwargs):
    """Ввод персональных данных."""
    serializer = PersonalInfoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_id = kwargs["user_id"]
    user = CustomUser.objects.filter(id=user_id).first()

    if request.method == "POST":
        user.username = serializer.validated_data["username"]  # Обязательное?
        # user.phone_number = serializer.validated_data["phone_number"]
        user.first_name = serializer.validated_data.get("first_name", "")
        user.last_name = serializer.validated_data.get("last_name", "")
        user.info = serializer.validated_data.get("info", "")
        user.is_first = False

        user.save()
        login(request, user)
        return redirect("bulletin:home")
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
def logout_view(request):
    """Выход из учетной записи пользователя."""
    logout(request)
    reffer = request.META.get("HTTP_REFERER")
    if reffer:
        return redirect(reffer)
    return redirect(reverse("bulletin:login"))

    # print(cache.get("user"))
    # if request.method == "POST":
    #     # user_id = request.session["user_id"]
    #     user = cache.get("user")
    #     serializer = OneTimeCodeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     print(user)
    #     user_code = OneTimeCode.objects.get(user=user)
    #     if serializer.validated_data["code"] == user_code:
    #         return redirect("bulletin:home")
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    # return Response(status=status.HTTP_200_OK)


# @api_view(["POST"])
# def login(request):
#     """Вход по одноразовому паролю."""
#     # serializer = LoginSerializer(data=request.data)
#     # serializer.is_valid(raise_exception=True)
#     # email = serializer.validated_data["email"]
#     # user, _ = CustomUser.objects.get_or_create(email=email)
#     #
#     # code = get_random_code()
#     # # send_code_by_email(email, code)
#     # # login(request, user)
#     # print(code)
#     # print(serializer.data)
#     # print(request)
#     # request.session["email"] = email
#     # request.session["code"] = code
#     # return redirect("bulletin:verify_code")
#     # return Response(serializer.data, status=status.HTTP_200_OK)
#     pass

@api_view(["POST", "GET"])
@permission_classes((permissions.IsAuthenticated,))
def verify_code(request):
    """Подтверждение одноразового пароля."""
    # print(request.session["email"])
    # print(request.session["code"])
    # return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
