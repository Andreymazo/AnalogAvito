from rest_framework import serializers

from personal_account.models import Balance


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода баланса пользователя"""

    class Meta:
        model = Balance
        fields = ('balance', 'currency')
