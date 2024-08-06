from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from ad.models import Promotion
from users.models import CustomUser, Notification
from django.contrib.contenttypes.models import ContentType

@receiver(user_logged_in, sender=CustomUser)
def create_notification_for_logged_in(sender, user, request, **kwargs):
    print('user', user)
    print('sender', sender)
    print('type(user), user.id', type(user), user.id)

    object = user
    content_type=type(user)
    object_id=object.id
    promotion_qeryset = Promotion.objects.filter(content_type=type(user), object_id=object.id)#Выберем промоушены зарегистрировавшегося юзера
    # У Промоушена ключ на Профиль, у Профиля ключ на Юзера, Юзер входит, тут проверяется вся его подписка на подход к концу. CustomUser id = 32
    # ContentType
    content_object = ContentType.objects.get_for_model(user)#get_for_id(content_type).get_object_for_this_type(pk=object_id)
    print('-----------------content_object', content_object)
    for i in promotion_qeryset:
        if (i.time_paied - timezone.now()).days < 1:
            Notification.objects.create(text = f"less 1 day left for {ContentType.objects.get_for_id(i.content_type).get_object_for_this_type(pk=i.object_id)} promotion", key_to_recepient=object.email, user=CustomUser.objects.get(email="andreymazoo@mail.ru"))  #user от кого пришло, ставим суперюзера

user_logged_in.connect(create_notification_for_logged_in)

import logging

user_logger = logging.getLogger("user")

@receiver(user_logged_in)
def log_user_login(sender, user, ** kwargs):
    """ Log user login to user log """
    user_logger.info('%s login successful', user)

@receiver(user_login_failed)
def log_user_login_failed(sender, user = None, ** kwargs):
    """ Log user login failure to user log """
    if user:
        user_logger.info('%s login failed', user)
    else:
        user_logger.error('login failed; unknown user')

@receiver(user_logged_out)
def log_user_logout(sender, user, ** kwargs):
    """ Log user logout to user log """
    user_logger.info('%s logout successful', user)