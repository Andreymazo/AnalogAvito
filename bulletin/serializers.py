from rest_framework import serializers
from config.constants import MAX_LEN_CODE, MAX_LEN_EMAIL
from ad.models import  Car, Category, Images, Advertisement
from users.models import CustomUser, OneTimeCode, Profile


class AlternativeAuthSerializer(serializers.Serializer):
    user_input_value = serializers.CharField()

# class ProfileRegistrationSerializer():
#     class Meta:
#         model = Profile
#         fields = "phone_number",#"phone_number"

# class CustomUserLoginSerializer(serializers.ModelSerializer):
#     """Сериализатор для входа по одноразовому коду."""
#     email = serializers.EmailField(max_length=MAX_LEN_EMAIL)
#     profile = ProfileRegistrationSerializer()
#     # phone_number = serializers.CharField(source='profile.phone_number')
    
#     class Meta:
#         """Конфигурация сериализатора для входа по одноразовому коду."""
#         model = CustomUser
#         fields = ['email', 'profile',]# 'phone_number']
#         # fields = ("email", "phone",)  # "username")
#         # read_only_fields = ("username",)
#         # read_only_fields = ("username",)
        
    def create(self, validated_data):
        print('nnnnnnnnnnnnnnnnnnnnnnnnnnn')
        profile_data = validated_data.pop('profile')
        user = CustomUser.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

class SignInSerializer(serializers.ModelSerializer):
    """Сериализатор для представления пользователя после входа."""

    class Meta:
        model = CustomUser
        fields = ("id", "email")
        read_only_fields = ("id", "email")


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        """Конфигурация сериализатора для регистрации пользователя."""
        model = Profile
        fields = ("user", "name", "phone_number", "location")
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = self.context["user"]
        profile = Profile.objects.create(
            user=user,
            name=validated_data["name"],
            phone_number=validated_data["phone_number"],
            location=validated_data["location"]
        )
        profile.save()
        return profile


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     """Сериализатор для модели пользователя."""

#     class Meta:
#         """Конфигурация сериализатора для пользователя."""
#         model = CustomUser
#         fields = ("email", "password")
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         """Создание пароля."""
#         user = CustomUser(email=validated_data["email"])
#         user.set_password(validated_data["password"])
#         user.save()
#         return user


class OneTimeCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели одноразового кода."""
    code = serializers.CharField(max_length=MAX_LEN_CODE)

    class Meta:
        """Конфигурация сериализатора для одноразового кода."""
        model = OneTimeCode
        fields = ("code",)


# class CreateProfileSerializer(serializers.ModelSerializer):
#     """Сериализатор для ввода персональных данных."""

#     class Meta:
#         """Конфигурация сериализатора для ввода персональных данных."""
#         model = CustomUser
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             # "phone_number",
#             "info"
#         )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileSerializerCarUpdate(serializers.ModelSerializer):
    Profile._meta.get_field('id')._unique = False
    class Meta:
        model = Profile
        # fields = "__all__"
        fields = ("id",)
        

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""

    class Meta:
        """Сериализатор для категории."""
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "level"
        )

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields["children"] = CategorySerializer(many=True, required=False)
        return fields

class AdvertisementSerializer(serializers.Serializer):

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ('created', 'changed')

class ImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Images
        fields = ("title", "profile", "image" )

   
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth import get_user_model
class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
        image = serializers.ImageField( write_only=True )
        title = serializers.CharField(write_only=True)
    
        class Meta:
            model = Car
            fields = ("id", "by_mileage", "category_id", 'brand', "year", "model", "mileage", "price", "image", "title", )

        def create(self, validated_data):
            # user=get_user_model()
            car_instance, created = Car.objects.get_or_create(
                by_mileage=validated_data.get('by_mileage', None),
                year=validated_data.get('year', None), 
                brand=validated_data.get('brand',None), 
                model=validated_data.get('model', None), 
                mileage=validated_data.get('mileage', None),
                price=validated_data.get('price',None), 
                category_id=Category.objects.get(name='Транспорт',).id,
                profile = Profile.objects.get(user=self.context['request'].user),
                )
           
            image_instance, created = Images.objects.get_or_create(
                content_type = ContentType.objects.get_for_model(car_instance),
                object_id = car_instance.id,
                title=validated_data.get('title'),
                image = validated_data.get('image'),#validated_data.get('image'),# validated_data.get('image'), 
                profile =validated_data.get('profile'), 
            )        
            return car_instance, image_instance
        
        def update(self, instance, validated_data):
            return super().update(instance, validated_data)
     #     car_instance, created = Car.objects.get_or_create(
    #             by_mileage=serializer.validated_data.get('by_mileage', None),
    #             year=serializer.validated_data.get('year', None), 
    #             brand=serializer.validated_data.get('brand',None), 
    #             model=serializer.validated_data.get('model', None), 
    #             mileage=serializer.validated_data.get('mileage', None),
    #             price=serializer.validated_data.get('price',None), 
    #             category_id=Category.objects.get(name='Транспорт',).id,
    #             profile = Profile.objects.get(user=request.user)
    #             )#category_id=validated_data.get('category_id', None).id # Can choose
                
    #     try:
    #         #Photoes anyway will be loaded even the same
    #         image_instance, created = Images.objects.get_or_create(
    #                 content_type = ContentType.objects.get_for_model(type(car_instance)),object_id = car_instance.id,
    #                 title=serializer.validated_data.get('title'),image = serializer.validated_data.get('image'),
    #                 )
    #         # return Response( [serializer.data, {"message": "This photo already uploaded"}], status=status.HTTP_206_PARTIAL_CONTENT)
    #     except Images.MultipleObjectsReturned:
    #         image = Images.objects.filter(content_type = ContentType.objects.get_for_model(type(car_instance)),
    #                 object_id = car_instance.id,title=serializer.validated_data.get('title'),).order_by('id').first()  
   