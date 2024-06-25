from django.urls import include, path
from ad.apps import AdConfig
from ad.views import (
    CarList,
    CategoryList,
)

app_name = AdConfig.name

urlpatterns = [
   path("category_list/", CategoryList.as_view(), name="ad_list"),
   path("car_list/", CarList.as_view(), name="car_list"),
]

