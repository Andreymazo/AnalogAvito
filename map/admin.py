# from django.contrib.gis import admin
# from django.contrib.gis.admin import OSMGeoAdmin
# from map.models import Marker


# @admin.register(Marker)
# class MarkerAdmin(OSMGeoAdmin):
#     """Marker admin."""

#     list_display = ("name", "location")
from django.contrib.gis import admin

from map.models import Marker


@admin.register(Marker)
class MarkerAdmin(admin.GISModelAdmin):
    list_display = ("name", "location")
