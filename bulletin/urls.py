
from django.urls import path

from bulletin.apps import BulletinConfig
from bulletin.views import home

app_name = BulletinConfig.name

urlpatterns = [

    path('', home, name='home'),

]
