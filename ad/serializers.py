from rest_framework import serializers

from ad.models import Like, Notification


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class LikeSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["user"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
     