from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ad.models import IP, Car, Category, Images, Like
from bulletin.serializers import CarSerializer, ImagesSerializer, ProfileSerializer
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


class CarCreateSerializer(serializers.ModelSerializer):
    
    images =  ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = Car
        fields = ["category", "profile", "by_mileage", "brand", "model", "price", "year", "mileage", "transmission",\
                  "by_wheel_drive", "engine_capacity", "engine_power", "fuel_consumption", "type", "colour", "fuel",\
                      "images", "uploaded_images",]# ["year", "images", "uploaded_images", "mileage"] ["__all__"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        
        car = Car.objects.create(category_id=Category.objects.get(name='Транспорт',).id,**validated_data)

        for image in uploaded_images:
            images = Images.objects.create(profile=Profile.objects.get(user=self.context['request'].user), image=image, content_type=ContentType.objects.get_for_model(type(car)), object_id=car.id)
            images.save()
        return car
 