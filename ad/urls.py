from django.urls import include, path
from ad.apps import AdConfig
from ad.views import (
    CategoryList,
)

app_name = AdConfig.name

urlpatterns = [
   path("category_list/", CategoryList.as_view(), name="ad_list"),
]

