from rest_framework import serializers

from users.models import CustomUser, MAX_LEN_CODE, OneTimeCode


class CustomUserLoginSerializer(serializers.ModelSerializer):
    """Сериализатор для входа по одноразовому коду."""
    email = serializers.EmailField(max_length=254)

    class Meta:
        """Конфигурация сериализатора для входа по одноразовому коду."""
        model = CustomUser
        fields = ("email", "username")
        read_only_fields = ("username",)
        # read_only_fields = ("username",)


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


class CreateProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для ввода персональных данных."""

    class Meta:
        """Конфигурация сериализатора для ввода персональных данных."""
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            # "phone_number",
            "info"
        )
