from rest_framework import serializers

from config.constants import MAX_LEN_CODE
from users.models import Profile, CustomUser, OneTimeCode


class AlternativeAuthSerializer(serializers.Serializer):
    user_input_value = serializers.CharField()


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
        fields = ("user", "name", "phone_number", )
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


class OneTimeCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели одноразового кода."""
    code = serializers.CharField(max_length=MAX_LEN_CODE)

    class Meta:
        """Конфигурация сериализатора для одноразового кода."""
        model = OneTimeCode
        fields = ("code",)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileSerializerCarUpdate(serializers.ModelSerializer):
    Profile._meta.get_field('user')._unique = False

    class Meta:
        model = Profile
        # fields = "__all__"
        fields = ("user",)
