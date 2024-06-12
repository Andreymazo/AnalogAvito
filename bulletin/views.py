from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render, reverse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from bulletin.serializers import (OneTimeCodeSerializer)
from config.settings import ATTEMPTS
from users.models import CustomUser, OneTimeCode
from users.models import COUNT_ATTEMPTS, CustomUser, OneTimeCode

from bulletin.serializers import (CreateProfileSerializer,
                                  CustomUserLoginSerializer,
                                  OneTimeCodeSerializer)
from bulletin.utils import (check_ban,  create_code, get_random_code, if_user_first)

TIME_OTC = 30 * 60  # Время жизни кода в секундах

def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)




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
        email_code = create_code(user)  # Либо создаем, либо меняем поле code в существующем коде пользователя и отправлям на confirm_code
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
    if request.method == "POST":
       
        try:
            email = request.session["email"]
            user = CustomUser.objects.get(email=email)
            # email_code = request.session["email_code"]
            email_code = OneTimeCode.objects.get(user_id=user.id)
            print('email_code', email_code)
        except email.DoesNotExist or email_code.DoesNotExist: # Прилетел как-то без емэйла и без кода, редиректим его обратно на логин
            return redirect(reverse("bulletin:log_in"))
        user = CustomUser.objects.get(email=email)
        if not if_user_first(email) == True:# Если впервые зашел, перенаправим на регистрацию
            return Response(status=status.HTTP_200_OK) 
            # redirect(reverse("bulletin:sign_up"))

        formatted_ban_time = check_ban(user)
        if formatted_ban_time:
            return Response({
                "error": (f"Вы забанены на 24 часа. "
                          f"Осталось {formatted_ban_time}")
            })
        otc = user.onetimecodes
        attempts_passed = otc.count_attempts
        if otc.count_attempts > ATTEMPTS:
                user.is_banned = True
                user.save()
                return Response({
                    "error": (f"Вы ввели неправильно {attempts_passed} раза "
                              "Вы забанены на 24 часа")
                })
        
        serializer = OneTimeCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            email_code_value = serializer.validated_data["code"]
            # Проверяем срок действия кода, если просрочен, то отправляем снова
            if datetime.now(timezone.utc) - otc.updated_at > timedelta(
                seconds=TIME_OTC
            ):
                # otc.delete()
                create_code(user)  # Повторная отправка кода? 
                otc.count_attempts += 1
                otc.save()
                # надо прибавлять 1 к попыткам ,чтобы все время не отправлять код, если чел просто оставил тут все как есть
                return Response(
                    {"error": "Время ожидания истекло"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Если код подходит Проверяем пользователя:
            # если он впервые - отправляем заполнять данные, если нет - на главную
            if otc.code == email_code_value:
                otc.count_attempts += 1
                otc.save()
                login(request, user)
                return redirect(reverse("bulletin:home"))

            otc.count_attempts += 1
            return Response(
                {
                    "error": (f"Вы ввели код неправильно {attempts_passed} раза. "
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
