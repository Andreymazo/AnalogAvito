from django.urls import path
from ad.apps import AdConfig
from ad.views import (
    CarList,
    CategoryList,   
    UploadFileImage,
    UploadViewSet,
    like_list_create,

)
from django.urls import include, path

from rest_framework.routers import SimpleRouter
from ad.views import UploadViewSet


router = SimpleRouter()
router.register(r'upload', UploadViewSet, basename='upload')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

# from rest_framework import routers
# router = routers.DefaultRouter()
# router.register(r'upload', UploadViewSet)

app_name = AdConfig.name

urlpatterns = [
   path('', include(router.urls)), 
   path("upload_file_image/", UploadFileImage.as_view(), name="upload_file_image"), 
   path("category_list/", CategoryList.as_view(), name="ad_list"),
   path("car_list/", CarList.as_view(), name="car_list"),
   path("like_list_create/", like_list_create, name="like_list_create"),
   
]

