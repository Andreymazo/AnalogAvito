from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

NULLABLE = {'blank': True, 'null': True}


"""Message model - messages between users"""
class Mssg(models.Model):
    viewed = models.BooleanField(default=False)
    text = models.CharField(max_length=400)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='mssg', **NULLABLE)
    key_to_recepient = models.CharField(max_length=50, verbose_name='Enter id or email of the user', **NULLABLE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return self.key_to_recepient
