from rest_framework import viewsets
from rest_framework_gis import filters
from drf_spectacular.utils import (
    extend_schema_field,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    inline_serializer, extend_schema_view
)
from map.models import Marker
from map.serializers import (
    MarkerSerializer,
)

@extend_schema(
    tags=["Карта/ Map"],

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
