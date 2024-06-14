import random
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.core.mail import send_mail
from config.settings import ATTEMPTS
from users.models import COUNT_ATTEMPTS, CustomUser, OneTimeCode

LEN_CODE = 5
TIME_BAN = 24 * 60 * 60  # Время бана в секундах


def get_random_code():
    """Получить временный код из 5-ти цифр."""
    return "".join(random.sample("0123456789", LEN_CODE))


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


def reset_attempts(otc):
    """Сброс попыток по времени."""
    if (datetime.now(timezone.utc) - otc.updated_at).days > 1:
        otc.count_attempts = COUNT_ATTEMPTS
        otc.save()
    return otc


def check_ban(user):
    """Проверка бана пользователя."""
    formatted_ban_time = ""
    if user.is_banned:
        # time_from_ban - время, прошедшее с момента бана
        time_from_ban = datetime.now(timezone.utc) - user.changed_at

        if time_from_ban < timedelta(seconds=TIME_BAN):
            # ban_time - оставшееся время бана
            ban_time = timedelta(seconds=TIME_BAN) - time_from_ban
            formatted_ban_time = ":".join(str(ban_time).split(":")[:2])
        else:
            # Пользователь разбанен по истечении времени
            otc = OneTimeCode.objects.get(user=user)
            # user.onetimecodes.count_attempts = COUNT_ATTEMPTS  # протестировать! -> не сохраняет
            otc.count_attempts = COUNT_ATTEMPTS
            otc.save()
            user.is_banned = False
            user.save()
    # Возвращает пустую строку, если бан есть, или строку со значением оставшегося времени
    return formatted_ban_time


def create_or_update_code(user):
    """Создать одноразовый код."""
    # Nado proverit est li cod libo update libo create
    code = get_random_code()
    email = user.email
     # for test
    # send_code_by_email(email, code)

    try:
        otc = OneTimeCode.objects.get(user=user)
        otc.code = code
        # otc.count_attempts += 1
        otc.save(update_fields=["code"])  # Поменяли только поле code, remaining_attempts
    except OneTimeCode.DoesNotExist:
        otc = OneTimeCode.objects.create(user=user, code=code)  # создали новый код пользователя
        otc.save()
    print('otc.code', otc.code)
    return otc


def if_user_first( email):
    if email in [i.email for i in CustomUser.objects.all()]:
        return True
    