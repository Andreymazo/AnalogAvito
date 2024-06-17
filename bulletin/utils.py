import random
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.core.mail import send_mail
from config.settings import ATTEMPTS
from users.models import CustomUser, OneTimeCode

LEN_CODE = 5
# TIME_BAN = 24 * 60 * 60  # Время бана в секундах
TIME_BAN = 15


def get_random_code():
    """Получить временный код из 5-ти цифр."""
    return "".join([str(random.randint(0, 9)) for _ in range(LEN_CODE)])
    # return "".join(random.sample("0123456789", LEN_CODE))


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
    # formatted_ban_time = ""
    ban_time = ""
    if user.is_banned:
        # time_from_ban - время, прошедшее с момента бана
        time_from_ban = datetime.now(timezone.utc) - user.banned_at

        if time_from_ban < timedelta(seconds=TIME_BAN):
            # ban_time - оставшееся время бана
            ban_time = timedelta(seconds=TIME_BAN) - time_from_ban
            # formatted_ban_time = ":".join(str(ban_time).split(":")[:2])
        else:
            # Пользователь разбанен по истечении времени
            # try:
            #     otc = OneTimeCode.objects.get(user=user)
            # except OneTimeCode.DoesNotExist:
            #     return Response(
            #         {
            #             "message": (
            #                 "Пользователь с таким E-mail "
            #                 "еще не зарегистрирован"
            #             )
            #         },
            #         status=status.HTTP_404_NOT_FOUND
            #     )
            # user.onetimecodes.count_attempts = COUNT_ATTEMPTS  # протестировать! -> не сохраняет
            # otc = user.onetimecodes
            # otc = OneTimeCode.objects.get(user=user)
            otc = user.onetimecodes
            otc.count_attempts = 0
            otc.count_send_code = 0
            otc.save()
            user.is_banned = False
            user.save(update_fields=["is_banned"])
    # Возвращает пустую строку, если бана нет.
    # Если есть - строку со значением оставшегося времени.
    return ban_time


def create_or_update_code(user):
    """Создать одноразовый код."""
    # Nado proverit est li cod libo update libo create
    code = get_random_code()
    # email = user.email
     # for test
    # send_code_by_email(email, code)

    # try:
    #     otc = OneTimeCode.objects.get(user=user)
    #     # otc.code = code
    #     # otc.count_attempts += 1
    #     # otc.save(update_fields=["code"])  # Поменяли только поле code
    # except OneTimeCode.DoesNotExist:
    #     # создали новый код пользователя
    #     otc = OneTimeCode.objects.create(user=user)
    #     # otc.save()
    otc, _ = OneTimeCode.objects.get_or_create(user=user)
    otc.code = code
    # otc.count_attempts -= 1
    # otc.save(update_fields=["code", "count_attempts"])
    otc.save()
    print("code: ", code)
    return otc


def if_user_first(email):
    if email in [i.email for i in CustomUser.objects.all()]:
        return True
