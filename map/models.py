# from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db import models
NULLABLE = {'blank': True, 'null': True}

class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255)
    location = PointField()
   

