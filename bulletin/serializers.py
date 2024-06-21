from rest_framework import serializers

from ad.models import Advertisement, Category
from config.constants import MAX_LEN_CODE
from users.models import CustomUser, OneTimeCode, Profile


class CustomUserLoginSerializer(serializers.ModelSerializer):
    """Сериализатор для входа по одноразовому коду."""
    email = serializers.EmailField(max_length=254)

    class Meta:
        """Конфигурация сериализатора для входа по одноразовому коду."""
        model = CustomUser
        fields = ("email",)  # "username")
        # read_only_fields = ("username",)
        # read_only_fields = ("username",)


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
            # "level"
        )

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields["children"] = CategorySerializer(many=True, required=False)
        return fields


class AdvertisementSerializer(serializers.Serializer):

    title = serializers.CharField()
    description = serializers.CharField()
    profile = ProfileSerializer() 
    category = CategorySerializer(many=True)
    created = serializers.DateTimeField()
    changed = serializers.DateTimeField()
    moderation = serializers.BooleanField()

    # category = CategorySerializer()

    # class Meta:
    #     model = Advertisement
    #     fields = ()

