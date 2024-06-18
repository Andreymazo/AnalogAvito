import random
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.core.mail import send_mail
from users.models import OneTimeCode

from config.constants import LEN_CODE, TIME_BAN


def get_random_code():
    """Получить временный код из 5-ти цифр."""
    return "".join([str(random.randint(0, 9)) for _ in range(LEN_CODE)])


def send_code_by_email(email, code):
    """Отправить код на электронную почту."""
    message = f"Код: {code}"
    send_mail(
        subject="Временный код доступа",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return message


def check_ban(user):
    """Проверка бана пользователя."""
    ban_time = ""
    if user.is_banned:
        # time_from_ban - время, прошедшее с момента бана
        time_from_ban = datetime.now(timezone.utc) - user.banned_at

        if time_from_ban < timedelta(seconds=TIME_BAN):
            ban_time = user.banned_at + timedelta(seconds=TIME_BAN)
        else:
            otc = user.onetimecodes
            otc.count_attempts = 0
            otc.count_send_code = 0
            otc.save()
            user.is_banned = False
            user.save()
    # Возвращает пустую строку, если бана нет.
    # Если есть - строку со значением оставшегося времени.
    return ban_time


def create_or_update_code(user):
    """Создать одноразовый код."""
    code = get_random_code()

    otc, _ = OneTimeCode.objects.get_or_create(user=user)
    otc.code = code
    otc.save()
    print("code: ", code)
    return otc
