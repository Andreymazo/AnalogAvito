from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ad.models import IP, BagsKnapsacks, Car, Category, ChildClothesShoes, Images, Like, Favorite, MenClothes, MenShoes, Views, WemenClothes, WemenShoes
from bulletin.serializers import CarSerializer, ImagesSerializer, ProfileSerializer
from users.models import CustomUser, Notification, Profile



class ViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class LikeSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = [ "is_liked", ]


class FavoiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class FavoiteSrerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = [ "is_favorited", ]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class IpSerializer(serializers.ModelSerializer):
    class Meta:
        model=IP
        fields = ("profile",)


class CarCreateSerializer(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    
    # images_car_instance=ImagesSerializer()
    class Meta:
        model = Car
        fields = ["id", "title", "by_mileage", "brand", "model", "price", "year", "mileage", "transmission",\
                  "by_wheel_drive", "engine_capacity", "engine_power", "fuel_consumption", "type", "colour", "fuel",\
                       "image", "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======  mmmmmmm', validated_data)
        profile_instance = self.context['request'].user.profile
        car = Car(content_object = profile_instance, category_id=Category.objects.get(name='Автомобили',).id,**validated_data)
        car.save()
        # car , _ = Car.objects.get_or_create(profile = self.context['request'].user.profile, category_id=Category.objects.get(name='Транспорт',).id,**validated_data)
        
        for image in uploaded_images:
            images = Images( image=image, content_type=ContentType.objects.get_for_model(type(car)), object_id=car.id)
            images.save()
        return car
    #Update надо сделать отдельным сериалезатором, изза списка фотографий
    def update(self, instance, validated_data):
        print('================instsance ------------>', instance.images.all())
        print('================validated_data------------>', validated_data)
        print('================validated_data------------>', self.__dict__)
        image_queryset = instance.images.all()
        images_car_instance=ImagesSerializer(image_queryset, many=True)
        instance.by_mileage = validated_data.get('by_mileage', instance.by_mileage)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.price = validated_data.get('price', instance.price)
        instance.year = validated_data.get('year', instance.year)
        instance.mileage = validated_data.get('mileage', instance.mileage)
        instance.transmission = validated_data.get('transmission', instance.transmission)
        instance.by_wheel_drive = validated_data.get('by_wheel_drive', instance.by_wheel_drive)
        instance.engine_capacity = validated_data.get('engine_capacity', instance.engine_capacity)
        instance.engine_power = validated_data.get('engine_power', instance.engine_power)
        instance.fuel_consumption = validated_data.get('fuel_consumption', instance.fuel_consumption)
        instance.type = validated_data.get('type', instance.type)
        instance.colour = validated_data.get('colour', instance.colour)
        instance.fuel = validated_data.get('fuel', instance.fuel)
        instance.image = validated_data.get('image', instance.images)
        # instance.uploaded_images = validated_data.get('uploaded_images', instance.uploaded_images)
        print('end======================',)
       
        instance.save()

        return instance
     
class CarPatchSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Car
        fields = ["id", "title", "by_mileage", "brand", "model", "price", "year", "mileage", "transmission",\
                  "by_wheel_drive", "engine_capacity", "engine_power", "fuel_consumption", "type", "colour", "fuel",]

    def update(self, instance, validated_data):
        instance.by_mileage = validated_data.get('by_mileage', instance.by_mileage)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.price = validated_data.get('price', instance.price)
        instance.year = validated_data.get('year', instance.year)
        instance.mileage = validated_data.get('mileage', instance.mileage)
        instance.transmission = validated_data.get('transmission', instance.transmission)
        instance.by_wheel_drive = validated_data.get('by_wheel_drive', instance.by_wheel_drive)
        instance.engine_capacity = validated_data.get('engine_capacity', instance.engine_capacity)
        instance.engine_power = validated_data.get('engine_power', instance.engine_power)
        instance.fuel_consumption = validated_data.get('fuel_consumption', instance.fuel_consumption)
        instance.type = validated_data.get('type', instance.type)
        instance.colour = validated_data.get('colour', instance.colour)
        instance.fuel = validated_data.get('fuel', instance.fuel)
        instance.image = validated_data.get('image', instance.images)

        instance.save()
        return instance
            
            
class CarNameSerializer(serializers.ModelSerializer):
    # id = serializers.CharField()
    class Meta:
        model = Car
        fields = ["id",]


class DefaultSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)


class CategoryFilterSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и фильтрации категории."""

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "level")

    def get_fields(self):
        fields = super(CategoryFilterSerializer, self).get_fields()
        fields["children"] = CategoryFilterSerializer(many=True, required=False)
        return fields


class MenClothesSerialiser(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = MenClothes
        # fields = "__all__"
    
        fields = ["id", "size", "price", "title", "uploaded_images","image"]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        profile_instance = self.context['request'].user.profile
        instance_here = MenClothes(content_object = profile_instance, category_id=Category.objects.get(name='Мужская одежда',).id,**validated_data)
        instance_here.save()
        
        for image in uploaded_images:
            images = Images( image=image, content_type=ContentType.objects.get_for_model(type(instance_here)), object_id=instance_here.id)
            images.save()
        return instance_here
     

class WemenClothesSerialiser(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = WemenClothes
        fields = ["id", "price", "title", "uploaded_images","image"]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        profile_instance = self.context['request'].user.profile
        instance_here = WemenClothes(content_object = profile_instance, category_id=Category.objects.get(name='Женская одежда',).id,**validated_data)
        instance_here.save()
        
        for image in uploaded_images:
            images = Images( image=image, content_type=ContentType.objects.get_for_model(type(instance_here)), object_id=instance_here.id)
            images.save()
        return instance_here


class MenShoesSerialiser(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = MenShoes
        fields = ["id", "price", "title", "uploaded_images","image"]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        profile_instance = self.context['request'].user.profile
        instance_here = MenShoes(content_object = profile_instance, category_id=Category.objects.get(name='Мужская обувь',).id,**validated_data)
        instance_here.save()
        
        for image in uploaded_images:
            images = Images( image=image, content_type=ContentType.objects.get_for_model(type(instance_here)), object_id=instance_here.id)
            images.save()
        return instance_here
    

class WemenShoesSerialiser(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = WemenShoes
        fields = ["id", "price", "title", "uploaded_images","image"]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        profile_instance = self.context['request'].user.profile
        instance_here = WemenShoes(content_object = profile_instance, category_id=Category.objects.get(name='Женская обувь',).id,**validated_data)
        instance_here.save()
        
        for image in uploaded_images:
            images = Images( image=image, content_type=ContentType.objects.get_for_model(type(instance_here)), object_id=instance_here.id)
            images.save()
        return instance_here


class ChildClothesShoesSerialiser(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = ChildClothesShoes
        fields = ["id", "price", "title",  "uploaded_images","image"]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        profile_instance = self.context['request'].user.profile
        instance_here = ChildClothesShoes(content_object = profile_instance, category_id=Category.objects.get(name='Детская одежда и обувь',).id,**validated_data)
        instance_here.save()
        
        for image in uploaded_images:
            images = Images(image=image, content_type=ContentType.objects.get_for_model(type(instance_here)), object_id=instance_here.id)
            images.save()
        return instance_here
    

class BagsKnapsacksSerialiser(serializers.ModelSerializer):
    image = ImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = BagsKnapsacks
        fields = ["id", "price", "title", "uploaded_images","image"]
      
      
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        print('validated_data=======', validated_data)
        profile_instance = self.context['request'].user.profile
        instance_here = BagsKnapsacks(content_object = profile_instance, category_id=Category.objects.get(name='Сумки, рюкзаки, чемоданы',).id,**validated_data)
        instance_here.save()
        
        for image in uploaded_images:
            images = Images( image=image, content_type=ContentType.objects.get_for_model(type(instance_here)), object_id=instance_here.id)
            images.save()
        return instance_here
   