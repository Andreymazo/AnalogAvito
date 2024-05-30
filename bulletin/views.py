from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bulletin.serializers import LoginSerializer
from bulletin.utils import send_code_by_email


def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)


@api_view(["POST"])
def login(request):
    """Вход по одноразовому паролю."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    send_code_by_email(email)

    return Response(serializer.data, status=status.HTTP_200_OK)
