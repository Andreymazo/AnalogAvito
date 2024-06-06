import random

from django.conf import settings
from django.core.mail import send_mail

from users.models import OneTimeCode

LEN_CODE = 5


def get_random_code():
    """Получить временный код из 5-ти цифр."""
    return "".join(random.sample("0123456789", LEN_CODE))


def send_code_by_email(email, code):
    """Функция отправляет код на электронную почту."""
    message = f"Код: {code}"
    send_mail(
        subject="Временный код доступа",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return message


def create_otc(user):
    """Создать код."""
    code = get_random_code()
    email = user.email
    print(code)  # for test
    # send_code_by_email(email, code)
    otc, _ = OneTimeCode.objects.get_or_create(user=user)
    otc.code = code
    otc.save()

    return otc
