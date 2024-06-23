from django.urls import include, path
from rest_framework import routers

from bulletin.apps import BulletinConfig
from bulletin.views import (
    # AdvertisementList,
    CategoryViewSet,
    ConfirmCodeView,
    NewCodeView,
    home,
    #ad_list,
    log_out,
    SignInView,
    SignUpView,
    verify_code
)

app_name = BulletinConfig.name

router = routers.DefaultRouter()

router.register("categories", CategoryViewSet)

url_v1 = [
    path("verify_code/", verify_code, name="verify_code"),
    path("sign_in_email/", SignInView.as_view(), name="sign_in_email"),
    path("log_out/", log_out, name="log_out"),
    # path("create_profile/", create_profile, name="create_profile"),
    path("confirm_code/", ConfirmCodeView.as_view(), name="confirm_code"),
    path("sign_up_profile/", SignUpView.as_view(), name="sign_up_profile"),
    path("new_code/", NewCodeView.as_view(), name="new_code"),
    # path("get_new_code/", get_new_code, name="get_new_code"),
    # path("ad_list/", ad_list, name="ad_list"),
    # path("ad_list/", AdvertisementList.as_view(), name="ad_list"),
    
    path("", include(router.urls)),
]


urlpatterns = [
    path("home/", home, name="home"),
    path("v1/", include(url_v1)),
]
