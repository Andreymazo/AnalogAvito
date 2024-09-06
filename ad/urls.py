from django.urls import path
from ad.apps import AdConfig
from ad.views import (
    CarDetailGeneric,
    CarList,
    CategoryViewSet,
    GetModelFmCategoryView,
    GetObjFmModelView,
    UploadViewSet,
    get_ads_fm_user,
    like_add,
    # like_list_create,
    like_list_obj,
    like_list_user,
    notifications_by_enter, CategoriesFilter,

)
from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter
from ad.views import UploadViewSet

router = SimpleRouter()
router.register(r'upload', UploadViewSet, basename='upload')

router = DefaultRouter()
router.register("categories", CategoryViewSet)

app_name = AdConfig.name

urlpatterns = [
   path('', include(router.urls)), 
   # path("category_list/", CategoryList.as_view(), name="ad_list"),
   path("car_list/", CarList.as_view(), name="car_list"),
   path("get_model_fm_category/", GetModelFmCategoryView.as_view(), name="get_model_fm_category"),
#    path("get_object_fm_model/", get_object_fm_model, name="get_object_fm_model"),
   path("get_object_fm_model/", GetObjFmModelView.as_view(), name="get_object_fm_model"),
   
   #path("car_create/", CarCreate.as_view(), name="car_create"),
   #path("like_list_create/", like_list_create, name="like_list_create"), point for test
   path("like_list_obj/", like_list_obj, name="like_list_obj"),
   path("like_list_user/", like_list_user, name="like_list_user"),
   path("like_add/", like_add, name="like_add"),
   path("notifications_by_enter/", notifications_by_enter, name="notifications_by_enter"),
   path("car_detail_generic/<int:pk>", CarDetailGeneric.as_view(), name="car_detail_generic"),

    # Category_filter_test
    path('categories_filter/', CategoriesFilter.as_view(), name='categories_filter'),
    path('get_ads_fm_user/', get_ads_fm_user, name='get_ads_fm_user'),
    
   
]

