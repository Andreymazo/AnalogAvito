from django.urls import include, path

from bulletin.apps import BulletinConfig
from bulletin.views import confirm_code_view, home, login, login_view, logout_view, verify_code


app_name = BulletinConfig.name

urlpatterns = [
    # path("login/", login, name="login"),
    # path("verify_code/", verify_code, name="verify_code"),
    path('', home, name='home'),

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("confirm_code/", confirm_code_view, name="confirm_code"),

    # path(r'auth/', include('djoser.urls')),

]
