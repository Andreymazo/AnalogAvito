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
        fields = ("user", "name", "phone_number")
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = self.context["user"]
        profile = Profile.objects.create(
            user=user,
            name=validated_data["name"],
            phone_number=validated_data["phone_number"],
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

class ProfileSerializer():
    class Meta:
        fields = "__all__"

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
        # fields = ("category ", "profile", "created", "changed", "moderation")


#     title = serializers.CharField()
#     description = serializers.CharField()
#     profile = ProfileSerializer() 
#     category = CategorySerializer(many=True)
#     created = serializers.DateTimeField()
#     changed = serializers.DateTimeField()
#     moderation = serializers.BooleanField()

    # category = CategorySerializer()

    # class Meta:
    #     model = Advertisement
    #     fields = ()
# class ImagesImageSerializer():
#     class Meta:
#         model = Images
#         fields = ("image",)

class ImagesSerializer(serializers.ModelSerializer):
    # content_object = serializers.SerializerMethodField()
    class Meta:
        model = Images
        fields = ("title", "profile", "image" )

    # def get_content_object(self, obj):
    #     return 
class CarSerializer(serializers.ModelSerializer):#, ):AdvertisementSerializer,
        
        image = serializers.ImageField( write_only=True )
        title = serializers.CharField(write_only=True)
    
        class Meta:
            model = Car
            fields = ("by_mileage", "category_id", 'brand', "year", "model", "mileage", "price", "image", "title")

        # def create(self, validated_data):
        #     car_instance, created = Car.objects.get_or_create(
        #         by_mileage=validated_data.get('by_mileage', None),
        #         year=validated_data.get('year', None), 
        #         brand=validated_data.get('brand',None), 
        #         model=validated_data.get('model', None), 
        #         mileage=validated_data.get('mileage', None),
        #         price=validated_data.get('price',None), 
        #         category_id=Category.objects.get(name='Транспорт',).id,
        #         marker_id = Marker.objects.get()
        #         )#category_id=validated_data.get('category_id', None).id # В закомменченном выбираем из категорий
                
           
        #     image_instance, created = Images.objects.get_or_create(
        #         car=car_instance,
        #         # title = title_of_image_value,#validated_data.get('title_of_image'),# validated_data.get('title'),
        #         title=validated_data.get('title'),
        #         image = validated_data.get('image'),#validated_data.get('image'),# validated_data.get('image'), 
        #         # profile = image_value.get('profile'),# validated_data.get('profile'), 
        #     )        
        #     return car_instance, image_instance