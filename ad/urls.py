from django.urls import path
from ad.apps import AdConfig
from ad.views import (
    BagsKnapsacksDetailGeneric,
    BagsKnapsacksList,
    CarDetailGeneric,
    CarList,
    CategoryViewSet,
    ChildClothesShoesDetailGeneric,
    ChildClothesShoesList,
    GetModelFmCategoryView,
    GetObjFmModelView,
    MenClothesDetailGeneric,
    MenClothesList,
    MenShoesDetailGeneric,
    MenShoesList,   
    UploadViewSet,
    WemenClothesDetailGeneric,
    WemenClothesList,
    WemenShoesDetailGeneric,
    WemenShoesList,
    create_object_fm_model,
    general_detailed,
    get_ads_fm_user,
    get_qs_fm_model,
    like_add,
    # like_list_create,
    like_list_obj,
    like_list_user,
    notifications_by_enter, CategoriesFilter,
    views_list_obj,

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
    path("get_qs_fm_model/", get_qs_fm_model, name="get_qs_fm_model"),
    path("create_object_fm_model/", create_object_fm_model, name="create_object_fm_model"),
    path("get_object_fm_model/", GetObjFmModelView.as_view(), name="get_object_fm_model"),

   
   #path("car_create/", CarCreate.as_view(), name="car_create"),
   #path("like_list_create/", like_list_create, name="like_list_create"), point for test
    path("like_list_obj/", like_list_obj, name="like_list_obj"),
    path("like_list_user/", like_list_user, name="like_list_user"),
    path("like_add/", like_add, name="like_add"),
    path("notifications_by_enter/", notifications_by_enter, name="notifications_by_enter"),
   
    path("car_detail_generic/<int:pk>", CarDetailGeneric.as_view(), name="car_detail_generic"),
    # path("car_detail_generic/<int:pk>", MenShoesDetailGeneric.as_view(), name="car_detail_generic"),
    # path("car_detail_generic/<int:pk>", WemenClothesDetailGeneric.as_view(), name="car_detail_generic"),
    # path("car_detail_generic/<int:pk>", WemenShoesDetailGeneric.as_view(), name="car_detail_generic"),
    # path("car_detail_generic/<int:pk>", BagsKnapsacksDetailGeneric.as_view(), name="car_detail_generic"),
    # path("car_detail_generic/<int:pk>", ChildClothesDetailGeneric.as_view(), name="car_detail_generic"),
    # path("car_partial_update/<int:pk>", CarPartialUpdateAPIView.as_view(), name='car_partial_update'),
    path('view_list_obj', views_list_obj, name='view_list_obj'),
    path('categories_filter/', CategoriesFilter.as_view(), name='categories_filter'),
    
    path('men_clothes_list/', MenClothesList.as_view(), name='men_clothes_list'),
    path("men_clothes_detail_generic/<int:pk>", MenClothesDetailGeneric.as_view(), name="men_clothes_detail_generic"),
    path('men_shoes_list/', MenShoesList.as_view(), name='men_shoes_list'),
    path('men_shoes_detail_generic/<int:pk>', MenShoesDetailGeneric.as_view(), name='men_shoes_detail_generic'),
    path('wemen_clothes_list/', WemenClothesList.as_view(),  name='wemen_clothes_list'),
    path('wemen_clothes_detail_generic/<int:pk>', WemenClothesDetailGeneric.as_view(),  name='wemen_clothes_detail_generic'),
    path('wemen_shoes_list/', WemenShoesList.as_view(),  name='wemen_shoes_list'),
    path('wemen_shoes_detail_generic/<int:pk>', WemenShoesDetailGeneric.as_view(),  name='wemen_shoes_detail_generic'),
    path('bagsknapsack_list/', BagsKnapsacksList.as_view(), name='bagsknapsack_list'),
    path('bagsknapsack_detail_generic/<int:pk>', BagsKnapsacksDetailGeneric.as_view(), name='bagsknapsack_detail_generic'),
    path('childclothesshoes_list/', ChildClothesShoesList.as_view(), name='childclothesshoes_list'),
    path('childclothesshoes_detail_generic/<int:pk>', ChildClothesShoesDetailGeneric.as_view(), name='childclothesshoes_detail_generic'),

    path('get_ads_fm_user/', get_ads_fm_user, name='get_ads_fm_user'),
    path('general_detailed/', general_detailed, name='general_detailed'),
    
]
