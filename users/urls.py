# from django.urls import path
# from users.apps import UsersConfig
# from users.views import ViewsList, views_user
from django.urls import path, include

from users.apps import UsersConfig
from users.views import SignInView, NewCodeView, ConfirmCodeView, SignUpView, log_out

# app_name = UsersConfig.name


# urlpatterns = [
#     path("views_user", views_user, name="views_user"),
#     path("views_user_generic", ViewsList.as_view(), name="views_user_generic"),
# ]

app_name = UsersConfig.name

url_v1 = [
    path("sign_in_email/", SignInView.as_view(), name="sign_in_email"),
    path("new_code/", NewCodeView.as_view(), name="new_code"),
    path("confirm_code/", ConfirmCodeView.as_view(), name="confirm_code"),
    path("sign_up_profile/", SignUpView.as_view(), name="sign_up_profile"),
    path("log_out/", log_out, name="log_out"),


    # path("verify_code/", verify_code, name="verify_code"),
    # # path("create_profile/", create_profile, name="create_profile"),
]

urlpatterns = [
    path('api/v1/', include(url_v1))
]
