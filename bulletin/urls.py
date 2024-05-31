from django.urls import include, path

from bulletin.apps import BulletinConfig
from bulletin.views import confirm_code, home, login_view, verify_code


app_name = BulletinConfig.name

urlpatterns = [
    # path("login/", login, name="login"),
    # path("verify_code/", verify_code, name="verify_code"),
    path('', home, name='home'),

    path("login/", login_view, name="login"),
    path("confirm_code/<int:user_id>/", confirm_code, name="confirm_code"),

    # path(r'auth/', include('djoser.urls')),

]
