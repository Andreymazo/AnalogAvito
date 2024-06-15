from django.urls import include, path
from rest_framework import routers

from bulletin.apps import BulletinConfig
from bulletin.views import (
    CategoryViewSet,
    ConfirmCodeView,
    # confirm_code,
    # create_profile,
    home,
    # sign_in,
    log_out,
    SignInView,
    SignUpView,
    # sign_up,
    verify_code
)

app_name = BulletinConfig.name

router = routers.DefaultRouter()

router.register("categories", CategoryViewSet)

url_v1 = [
    path("verify_code/", verify_code, name="verify_code"),
    path("sign_in/", SignInView.as_view(), name="sign_in"),
    path("log_out/", log_out, name="log_out"),
    # path("create_profile/", create_profile, name="create_profile"),
    path("confirm_code/", ConfirmCodeView.as_view(), name="confirm_code"),
    path("sign_up/", SignUpView.as_view(), name="sign_up"),
    # path("get_new_code/", get_new_code, name="get_new_code"),
    path("", include(router.urls)),
]


urlpatterns = [
    path("v1/", include(url_v1)),
    path("", home, name="home"),
]
