from rest_framework import viewsets
from rest_framework_gis import filters

from map.models import Marker
from map.serializers import (
    MarkerSerializer,
)

class MarkerViewSet(
    viewsets.ModelViewSet
):
    bbox_filter_field = "location"
    filter_backends = (
        filters.InBBoxFilter,
    )
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
