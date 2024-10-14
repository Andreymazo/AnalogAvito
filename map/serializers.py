from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
)
from rest_framework import serializers
from map.models import Marker
from users.models import Profile
# from drf_extra_fields.geo_fields import PointField # if needed ---- pip install drf-extra-fields

class MarkerSerializer(
    GeoFeatureModelSerializer
):
    profile_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=False)
    class Meta:
        fields = ( "name", "profile_id")
        geo_field = "location"
        model = Marker
        
    def create(self, validated_data):
        marker_instance, created = Marker.objects.get_or_create(
                name=validated_data.get('name', None), profile_id=validated_data.get('profile_id').id, location=validated_data.get('location'))
        return marker_instance