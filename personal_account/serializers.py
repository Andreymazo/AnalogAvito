from rest_framework import serializers

from ad.models import Car, MenClothes, WemenClothes, MenShoes, WemenShoes, ChildClothesShoes, BagsKnapsacks
from bulletin.serializers import ImagesSerializer, CategorySerializer
from personal_account.models import Balance


def choose_serializer(name):
    """Выбирает подходящий сериализатор на основе имени модели."""

    MODEL_SERIALIZERS = {
        "WemenClothes": WomenClothesForAccountSerializer,
        "MenShoes": MenShoesForAccountSerializer,
        "WemenShoes": WomenShoesForAccountSerializer,
        "ChildClothesShoes": ChildClothesShoesForAccountSerializer,
        "BagsKnapsacks": BagsKnapsacksForAccountSerializer,
        "Car": CarForAccountSerializer,
        "MenClothes": MenClothesForAccountSerializer,
    }

    return MODEL_SERIALIZERS[name]


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода баланса пользователя"""

    class Meta:
        model = Balance
        fields = ('balance', 'currency')


class CarForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Car
        fields = (
            'id', 'category', 'title', 'description', 'images', 'moderation', 'archived',
            'price', 'brand', 'model', 'year', 'by_mileage', 'mileage', 'transmission', 'by_wheel_drive',
            'engine_capacity', 'engine_power', 'fuel_consumption', 'location', 'type', 'colour', 'fuel',
            'created', 'changed', )


class WomenClothesForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = WemenClothes
        fields = (
            'id', 'category', 'title', 'description', 'images', 'moderation', 'archived',
            'price', 'created', 'changed',)


class MenShoesForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenShoes
        fields = (
            'id', 'category', 'title', 'description', 'images', 'moderation', 'archived',
            'price', 'created', 'changed',)


class WomenShoesForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = WemenShoes
        fields = (
            'id', 'category', 'title', 'description', 'images', 'moderation', 'archived',
            'price', 'created', 'changed',)


class ChildClothesShoesForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ChildClothesShoes
        fields = (
            'id', 'category', 'title', 'description', 'images', 'moderation', 'archived',
            'price', 'created', 'changed',)


class BagsKnapsacksForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = BagsKnapsacks
        fields = (
            'id', 'category', 'title', 'description', 'images', 'moderation', 'archived',
            'price', 'created', 'changed',)


class MenClothesForAccountSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода объявлений в ЛК"""

    images = ImagesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenClothes
        fields = (
            'id', 'category', 'title', 'description', 'size', 'images', 'moderation', 'archived',
            'price', 'created', 'changed',)
