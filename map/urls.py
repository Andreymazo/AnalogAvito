from django.urls import include, path
# from rest_framework import routers
from map.apps import MapConfig
from map.views import MarkersMap, MarkersMapView, query_rus_city

app_name = MapConfig.name

from rest_framework import routers

from map.viewsets import MarkerViewSet

router = routers.DefaultRouter()
router.register(r"markers", MarkerViewSet)

urlpatterns = router.urls

urlpatterns = [
    path("", MarkersMapView.as_view()),
    path("mm/", MarkersMap),
    path("markers",MarkerViewSet.as_view({'get': 'list', 'post':'create'})),
    path('query_rus_city/', query_rus_city, name='query_rus_city'),
]

# api2/markers/ 