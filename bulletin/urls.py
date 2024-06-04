from django.urls import include, path

from bulletin.apps import BulletinConfig
from bulletin.views import (confirm_code, home, login_view, logout_view, personal_info, verify_code)

app_name = BulletinConfig.name

urlpatterns = [
    # path("login/", login, name="login"),
    path("verify_code/", verify_code, name="verify_code"),
    path('', home, name='home'),
    # path("v1/drf-auth/", include("rest_framework.urls")),
    path("v1/login/", login_view, name="login"),
    path("v1/logout/", logout_view, name="logout"),
    path("v1/confirm_code/<int:user_id>/", confirm_code, name="confirm_code"),
    path("v1/personal_info/<int:user_id>/", personal_info, name="personal_info"),

    # path(r'auth/', include('djoser.urls')),

]
