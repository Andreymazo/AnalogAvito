from django.urls import include, path

from bulletin.apps import BulletinConfig
from bulletin.views import home, login


app_name = BulletinConfig.name

urlpatterns = [
    path("login/", login, name="login"),
    path('', home, name='home'),
    # path(r'auth/', include('djoser.urls')),

]
