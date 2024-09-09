import datetime

from django.db.models import Q
from django.utils.timezone import now

from ad.models import Car, Views, MenClothes, WemenClothes, MenShoes, WemenShoes, ChildClothesShoes, BagsKnapsacks
from config.celery import app
from users.models import CustomUser, Profile
from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task(name="count_profile_view_send_email")
def count_profile_view_send_email(i):
    users_total_views = Views.objects.filter(profile=i)
    users_car_views = users_total_views.filter(content_type=10)
    # res = send_mail(
    #     subject='advertisement vies statement',
    #     message=f'Your advertisements has total {users_total_views.count()} views, {users_car_views.count()} car views',
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[i.user.email, ],
    #     fail_silently=False,
    #     auth_user=None,
    # )
    """In future Mailing Log model can be implemented"""
    # Mailinglog.objects.create(


#                     message=f'Your advertisement has {users_views} views',
#                     mailing=i.user.email,
#                     result=res
#                 )
# [count_profile_view_send_email(i) for i in Profile.objects.all()]


@app.task(name='checking_before_archiving')
def checking_before_archiving():
    """Ежедневная проверка даты создания, при достижении дельты в 30 дней, объявление отправляется в архив"""

    # Список всех моделей объявлений
    advertisements = [Car, MenClothes, WemenClothes, MenShoes, WemenShoes, ChildClothesShoes, BagsKnapsacks]

    # time_life - время, прошедшее с создания объявления
    time_life = now() - datetime.timedelta(days=30)

    for advertisement in advertisements:
        advertisement.objects.filter(Q(archived=False), Q(created__lte=time_life)).update(archived=True)
        print('процесс идет')
