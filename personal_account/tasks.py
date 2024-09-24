from decimal import Decimal

import requests
from celery import shared_task
from personal_account.models import Currencies
from personal_account.utils import check_currencies_exists


@shared_task(name='get_currency')
def get_currency():
    """Ежедневное получение курса валют"""

    check_currencies_exists()

    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD,EUR&base=RUB"

    headers = {
        # Потом добавить в .env-файл
        "apikey": "WZtamIy4WAfuCTjyScokhymWWOAu70eJ"
    }

    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'rates' in data:
            rates = data['rates']

            try:
                usd_rate = 1 /Decimal(rates['USD'])
                eur_rate = 1/ Decimal(rates['EUR'])

                # Ограничиваем количество знаков после запятой до 2
                usd_rate = usd_rate.quantize(Decimal('0.01'))
                eur_rate = eur_rate.quantize(Decimal('0.01'))

                # Обновляем данные в БД
                Currencies.objects.update(usd_rate=usd_rate, eur_rate=eur_rate)

            except KeyError:
                print("Не удалось получить курсы валют")

        else:
            print("Ответ не соответствует ожидаемому")

    except Exception:
        print(f"Произошла ошибка")
