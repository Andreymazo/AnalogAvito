from django.urls import include, path

from bulletin.apps import BulletinConfig
from bulletin.views import (confirm_code, get_new_code, home, log_in, log_out,
                            sign_up, verify_code, create_profile)

app_name = BulletinConfig.name

url_v1 = [
    path("verify_code/", verify_code, name="verify_code"),
    path("log_in/", log_in, name="log_in"),
    path("log_out/", log_out, name="log_out"),
    path("create_profile/", create_profile, name="create_profile"),
    path("confirm_code/", confirm_code, name="confirm_code"),
    path("sign_up/", sign_up, name="sign_up"),
    path("get_new_code/", get_new_code, name="get_new_code")
]


urlpatterns = [
    path("v1/", include(url_v1)),
    path('', home, name='home'),
]
