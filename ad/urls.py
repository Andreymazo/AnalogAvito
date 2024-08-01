from django.urls import path
from ad.apps import AdConfig
from ad.views import (
    CarDetailGeneric,
    CarList,
    CategoryList, 
    UploadViewSet,
    like_add,
    # like_list_create,
    like_list_obj,
    like_list_user,
    notifications_by_enter,

)
from django.urls import include, path

from rest_framework.routers import SimpleRouter
from ad.views import UploadViewSet


router = SimpleRouter()
router.register(r'upload', UploadViewSet, basename='upload')


app_name = AdConfig.name

urlpatterns = [
   path('', include(router.urls)), 
   path("category_list/", CategoryList.as_view(), name="ad_list"),
   path("car_list/", CarList.as_view(), name="car_list"),
#    path("like_list_create/", like_list_create, name="like_list_create"), point for test
   path("like_list_obj/", like_list_obj, name="like_list_obj"),
   path("like_list_user/", like_list_user, name="like_list_user"),
   path("like_add/", like_add, name="like_add"),
   path("notifications_by_enter/", notifications_by_enter, name="notifications_by_enter"),
   path("car_detail_generic/<int:pk>", CarDetailGeneric.as_view(), name="car_detail_generic"),
   
]

