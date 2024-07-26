from rest_framework import serializers

from ad.models import Like
from users.models import Notification



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
     