from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings

CURRENCY = [
    ("RUB", "RUBLES"),
    ("USD", "DOLLARS"),
    ("EUR", "EURO"),
]

STATUS = [
    ("PENDING", "PENDING"),
    ("COMPLETED", "COMPLETED"),
    ("FAILED", "FAILED")
]

class Currencies(models.Model):
    """Валюта"""
    usd_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name='1 доллар')
    eur_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name='1 евро')

    class Meta:
        verbose_name = _('Валюта')
        verbose_name_plural = _('Валюты')

    def __str__(self):
        return str(self.usd_rate)



class Balance(models.Model):
    """Баланс пользователя по умолчанию 0, валюта рубли,
    создается в момент регистрации нового пользователя"""

    balance = models.DecimalField(max_digits=9,
                                  decimal_places=2,
                                  default=0,
                                  verbose_name='Баланс пользователя')
    currency = models.CharField(max_length=3,
                                choices=CURRENCY,
                                default='RUB')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='balance',
                                 verbose_name='Владелец баланса')


    class Meta:
        verbose_name = _('Баланс')
        verbose_name_plural = _('Балансы')

    def __str__(self):
        return str(self.balance)

    @property
    def get_balance_in_currency(self):

        currencies = Currencies.objects.all().first()

        usd = currencies.usd_rate
        eur = currencies.eur_rate

        # Делаем проверку какая валюта записана в базе на данный момент и возвращаем баланс в этой валюте
        if self.currency == 'USD':
            return self.balance / usd
        elif self.currency == 'EUR':
            return self.balance / eur
        else:
            return self.balance


class Payments(models.Model):
    """Платежи пользователя"""
    amount = models.DecimalField(max_digits=9,
                                 decimal_places=2,
                                 default=0,
                                 verbose_name='Сумма платежа')
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING', verbose_name='Статус платежа')
    creating_payment = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания платежа")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name='payments',
                                 verbose_name='Владелец платежа')

    class Meta:
        verbose_name = _('Платеж')
        verbose_name_plural = _('Платежи')
        ordering = ['-creating_payment']

    def __str__(self):
        return f"{self.amount} - {self.status}"
