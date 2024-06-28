from django.urls import include, path
# from rest_framework import routers
from map.apps import MapConfig
from map.views import MarkersMap, MarkersMapView

app_name = MapConfig.name


urlpatterns = [
    path("", MarkersMapView.as_view()),
    path("mm/", MarkersMap),

]

# api2/markers/ 