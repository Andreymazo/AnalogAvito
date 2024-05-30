from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа по одноразовому коду."""
    email = serializers.EmailField(max_length=254)
