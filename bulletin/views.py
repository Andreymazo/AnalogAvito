from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.shortcuts import redirect, render, reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bulletin.serializers import LoginSerializer, OneTimeCodeSerializer
from bulletin.utils import send_code_by_email, get_random_code
from users.models import CustomUser, OneTimeCode


def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)


@api_view(["POST"])
def login_view(request):
    """Вход по одноразовому коду."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if request.method == "POST":
        email = serializer.validated_data["email"]
        user, _ = CustomUser.objects.get_or_create(email=email)

        code = get_random_code()
        # send_code_by_email(email, code)
        one_time_code = OneTimeCode.objects.create(user=user, code=code)
        one_time_code.save()

        return redirect(reverse("bulletin:confirm_code", kwargs={"user_id": user.id}))
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
def confirm_code(request, **kwargs):
    """Подтверждение кода."""
    user_id = kwargs["user_id"]
    print(user_id)
    serializer = OneTimeCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email_code = serializer.validated_data["code"]
    user = CustomUser.objects.filter(id=user_id).first()

    otc = OneTimeCode.objects.filter(user=user, code=email_code).first()

    if otc and otc.code == email_code:
        login(request, user)
    else:
        return Response(
            {"error": "Invalid code"},
            status=status.HTTP_400_BAD_REQUEST
        )

    return redirect("bulletin:home")


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
def verify_code(request):
    """Подтверждение одноразового пароля."""
    # print(request.session["email"])
    # print(request.session["code"])
    # return Response(status=status.HTTP_200_OK)
    pass


