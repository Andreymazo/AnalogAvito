from rest_framework import serializers

from ad.models import IP, Car, Like
from bulletin.serializers import CarSerializer, ProfileSerializer
from users.models import Notification, Profile



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class LikeSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["user", "content_type", "object_id", "is_liked"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class IpSerializer(serializers.ModelSerializer):
    class Meta:
        model=IP
        fields = ("profile",)
 