import random
import re
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail

from config import settings
from config.constants import LEN_CODE, TIME_BAN
from users.models import OneTimeCode


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

"""Str on enter tru false in end Format +7932222334 or +7(921)321122223 len fm 6 to 15"""
def validate_phone(s):
    # digits=['0','1','2','3','4','5','6','7','8','9']
    try:
        # print('cheking phone', s, 's2=', s[2],'s6=', s[6],)
        # print('len(s)', len(s))
        if len(s) > 15 or len(s) < 6:
            # print('len ------------')
            return False 
        if s[0]!='+' and s[1]!='7':
            # print('1')
            return False
        if bool(re.search(r'^[0-9]*\Z', s[1:]))==True:#Если находит хоть одну букву False
            return True
        if s[2]!="(" or s[6]!=")":
            # print('s2=', s[2],'s6=', s[6], '2')
            return False
    
        else:
            print('end')
            return True
    except IndexError as e:
        print(e, 'Index out of range')


"""Проверяет то, что ввел пользователь, возвращает емэйл и телефон с соответсвующими флагами"""
def check_email_phone(s: str):
    """Функция проверки, что ввел пользователь"""
    pat_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # pat_phone = r"^(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"#^[+]{1}(?:[0-9\-\(\)\/\.]\s?){6, 15}[0-9]{1}$
    pat_phone = r"^[+]{1}(?:[0-9\-\(\)\/\.]\s?){6, 15}[0-9]{1}$"#\+7|8)\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}
    pat_phone = r"^\+7|8\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}"
    if re.match(pat_email, s):
        print("Valid Email")
        return (s, "email")
    if validate_phone(s) == True:

    # if re.match(pat_phone, s):
        print('Valid phone')
        return (s, "phone")
    else:
        print("Invalid Email and Phone")
        return (None, None)
