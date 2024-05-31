from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
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
    error_message = ""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    user, _ = CustomUser.objects.get_or_create(email=email)
    login(request, user)

    code = get_random_code()
    # send_code_by_email(email, code)
    one_time_code = OneTimeCode.objects.create(user=user, code=code)

    return redirect("bulletin:confirm_code")

    # return Response(serializer.data, status=status.HTTP_200_OK)


# def logout_view(request):
#     pass


@api_view(["POST", "GET"])
def confirm_code_view(request):
    """Подтверждение кода."""
    print(request.user)
    if request.method == "POST":
        serializer = OneTimeCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(request.user)
        user_code = OneTimeCode.objects.get(user=request.user)
        if serializer.validated_data["code"] == user_code:
            return redirect("bulletin:home")
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)



@api_view(["POST"])
def login(request):
    """Вход по одноразовому паролю."""
    # serializer = LoginSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # email = serializer.validated_data["email"]
    # user, _ = CustomUser.objects.get_or_create(email=email)
    #
    # code = get_random_code()
    # # send_code_by_email(email, code)
    # # login(request, user)
    # print(code)
    # print(serializer.data)
    # print(request)
    # request.session["email"] = email
    # request.session["code"] = code
    # return redirect("bulletin:verify_code")
    # return Response(serializer.data, status=status.HTTP_200_OK)
    pass


@api_view(["POST", "GET"])
def verify_code(request):
    """Подтверждение одноразового пароля."""
    # print(request.session["email"])
    # print(request.session["code"])
    # return Response(status=status.HTTP_200_OK)
    pass


