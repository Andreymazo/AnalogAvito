from django.urls import path

from bulletin.apps import BulletinConfig
from bulletin.views import (confirm_code, get_new_code, home, log_in, log_out,
                            sign_up, verify_code, create_profile)

app_name = BulletinConfig.name

urlpatterns = [
    # path("login/", login, name="login"),
    path("verify_code/", verify_code, name="verify_code"),
    path('', home, name='home'),
    path("v1/log_in/", log_in, name="log_in"),
    path("v1/log_out/", log_out, name="log_out"),
    path("v1/create_profile/", create_profile, name="create_profile"),
    # path("v1/confirm_code/<int:user_id>/", confirm_code, name="confirm_code"),
    path("v1/confirm_code/", confirm_code, name="confirm_code"),
    path("v1/sign_up/", sign_up, name="sign_up"),
    path("v1/get_new_code/", get_new_code, name="get_new_code")
]
