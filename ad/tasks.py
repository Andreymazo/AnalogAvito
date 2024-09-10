import datetime

from django.db.models import Q
from django.utils.timezone import now

from ad.models import Car, Views, MenClothes, WemenClothes, MenShoes, WemenShoes, ChildClothesShoes, BagsKnapsacks
from config.celery import app
from users.models import CustomUser, Profile
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

@shared_task(name="count_profile_view_send_email")
def count_profile_view_send_email():
    for i in Profile.objects.all():
        users_total_views_profile = Views.objects.filter(profile=i)
        app_models = apps.get_app_config('ad').get_models()
        for j in app_models:
        
            print('jjjjjjjjjj  iiii', j, i)
            users_total_views_profile_object = users_total_views_profile.filter(content_type=ContentType.objects.get_for_model(j))
            print(f" For  {i.name}. Model {j.__name__}. Number of views {users_total_views_profile_object.count()} ", )
      
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
# 


@shared_task(name='checking_before_archiving')
def checking_before_archiving():
    """Ежедневная проверка даты создания, при достижении дельты в 30 дней, объявление отправляется в архив"""
    # Список всех моделей объявлений
    advertisements = [Car, MenClothes, WemenClothes, MenShoes, WemenShoes, ChildClothesShoes, BagsKnapsacks]

    # time_life - время, прошедшее с создания объявления
    time_life = now() - datetime.timedelta(days=30)

    for advertisement in advertisements:
        advertisement.objects.filter(Q(archived=False), Q(created__lte=time_life)).update(archived=True)
