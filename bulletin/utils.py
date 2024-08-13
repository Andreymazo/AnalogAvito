import random
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.core.mail import send_mail
from users.models import OneTimeCode
from config.constants import LEN_CODE, TIME_BAN
import re

"""Get simple jwt token"""


# from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
