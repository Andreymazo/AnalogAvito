from datetime import datetime, timedelta, timezone

# from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, reverse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import COUNT_ATTEMPTS, CustomUser, OneTimeCode

from bulletin.serializers import (CreateProfileSerializer,
                                  CustomUserLoginSerializer,
                                  OneTimeCodeSerializer)
from bulletin.utils import (check_ban, get_random_code, reset_attempts,
                            send_code_by_email)

TIME_OTC = 30 * 60  # Время жизни кода в секундах


def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)


def create_code(user):
    """Создать одноразовый код."""
    # Nado proverit est li cod libo update libo create
    code = get_random_code()
    email = user.email
    print(code)  # for test
    # send_code_by_email(email, code)

    try:
        otc = OneTimeCode.objects.get(user=user)
        otc.code = code
        # otc.count_attempts += 1
        otc.save(update_fields=["code"])  # Поменяли только поле code, remaining_attempts
    except OneTimeCode.DoesNotExist:
        otc = OneTimeCode.objects.create(user=user, code=code)  # создали новый код пользователя
        otc.save()

    return otc

    # if user.onetimecodes:  # Обращаемся по обратному ключу onetimecodes, если код пользователя существует
    #     otc = OneTimeCode.objects.get(user=user)
    #     otc.code = code
    #     otc.remaining_attempts += 1
    #     otc.save(update_fields=['code', 'remaining_attempts'])  # Поменяли только поле code, remaining_attempts
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


@api_view(["GET", "POST"])
def sign_up(request):
    """Регистрация пользователя."""
    if request.method == "GET":
        serializer = CustomUserLoginSerializer()
        return Response({
            "data": serializer.data,
        })

    if request.method == "POST":
        serializer = CustomUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Если пользователя нет,то создаем его
            serializer.save(username=email, email=email)
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
        return redirect(reverse("bulletin:confirm_code"))


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
        login(request, user)
        return redirect(reverse("bulletin:home"))


@api_view(["GET", "POST"])
def log_in(request):
    """Вход по одноразовому коду."""
    if request.method == "GET":
        serializer = CustomUserLoginSerializer()
        return Response({
            "data": serializer.data,
        })

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

        create_code(user)  # Либо создаем, либо меняем поле code в существующем коде пользователя и отправлям на confirm_code
        request.session["email"] = email
        return redirect(reverse("bulletin:confirm_code"))


# добавить permission, если забанен - доступа нет
@api_view(["GET", "POST"])
def confirm_code(request):
    """Подтверждение кода."""
    if request.method == "GET":
        serializer = OneTimeCodeSerializer()
        return Response({
            "data": serializer.data,
        })

    if request.method == "POST":
        email = request.session["email"]
        # Забираем пользователя вместе с его кодом
        user = CustomUser.objects.select_related(
            "onetimecodes"
        ).get(email=email)
        otc = user.onetimecodes

        serializer = OneTimeCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_code = serializer.validated_data["code"]
        print(email_code)

        # Проверяем срок действия кода, если просрочен, то отправляем снова
        if datetime.now(timezone.utc) - otc.updated_at > timedelta(
            seconds=TIME_OTC
        ):
            # otc.delete()
            create_code(user)  # Повторная отправка кода?
            return Response(
                {"error": "Время ожидания истекло"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если код подходит, удаляем его из БД. Проверяем пользователя:
        # если он впервые - отправляем заполнять данные, если нет - на главную
        if otc.code == email_code:
            # otc.delete()
            # reffer = request.META.get("HTTP_REFERER")
            # if reffer:
            #     return redirect(reffer) -------- перенаправляет не так, как надо
            if user.is_first:
                user.is_first = False
                user.save()
                return redirect(reverse("bulletin:create_profile"))

            login(request, user)
            return redirect(reverse("bulletin:home"))

        # Проверяем, нужен ли сброс попыток по времени
        reset_attempts(otc)

        # if otc.count_attempts == 0:
        #     user.is_banned = True
        #     user.save()
        #     return Response({
        #         "error": (f"Вы ввели неправильно {attempts_passed} раза "
        #                   "Вы забанены на 24 часа")
        #     })

        otc.count_attempts -= 1
        otc.save()

        if otc.count_attempts != 0:
            return Response(
                {"error": "Неверный код"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # otc.delete()
        user.banned_at = datetime.now(timezone.utc)
        user.is_banned = True
        user.save()

        return Response(
            {
                "error": (f"Вы ввели код неправильно {COUNT_ATTEMPTS} раза. "
                          "Вы забанены на 24 часа")
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def get_new_code(request):
    """Запросить новый код."""
    email = request.session.get("email")
    if email:
        user = CustomUser.objects.get(email=email)
        # if datetime.now(timezone.utc) - otc.updated_at > timedelta(
        #     seconds=TIME_OTC
        # ):
        create_code(user)
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
