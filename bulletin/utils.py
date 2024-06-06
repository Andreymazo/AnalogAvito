import random

from django.conf import settings
from django.core.mail import send_mail

# from users.models import OneTimeCode

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


# def create_otc(user):
#     """Создать код."""
#     print("create_otc")
#     code = get_random_code()
#     email = user.email
#     print(code)  # for test
#     # send_code_by_email(email, code)
#     otc, _ = OneTimeCode.objects.get_or_create(user=user)
#     otc.code = code
#     otc.save()

#     return otc


# def ee():
#     """Проверка, забанен ли пользователь."""
#     email = request.session["email"]
#     print(email)  # for test
#     user = CustomUser.objects.get(email=email)

#     if user.is_banned:
#         ban_time = datetime.now(timezone.utc) - user.banned_at
#         if ban_time < timedelta(seconds=TIME_BAN):
#             formatted_ban_time = ":".join(str(ban_time).split(":")[:2])
#             return Response(
#                 {"error": (f"Вы забанены на 24 часа. "
#                            f"Осталось {formatted_ban_time}")}
#             )

#         user.is_banned = False
#         user.save()
#         print(f"Пользователь {user} разбанен по истечении времени.")  # for test

    # try:
    #     otc = OneTimeCode.objects.get(user=user)
    # except OneTimeCode.DoesNotExist:
    #     otc = create_otc(user)
