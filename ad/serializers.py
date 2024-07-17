from rest_framework import serializers

from ad.models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

class LikeSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ["user"]
     