from django.apps import apps

def check_currencies_exists():
    """Проверяем создана запись с валютами, если нет, то создаем"""

    currencies = apps.get_model('personal_account', 'Currencies')

    if not currencies.objects.exists():
        currencies.objects.create(usd_rate=1, eur_rate=1)