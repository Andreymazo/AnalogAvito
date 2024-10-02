from django.contrib import admin
from django.contrib.admin import ModelAdmin
from personal_account.models import Balance, Payments, Currencies


@admin.register(Balance)
class BalanceAdmin(ModelAdmin):
    list_display = ('balance', 'currency', 'profile',)

@admin.register(Payments)
class PaymentsAdmin(ModelAdmin):
    list_display = ('amount', 'status', 'creating_payment', 'user')
    list_display_links = ('amount',)

@admin.register(Currencies)
class CurrenciesAdmin(ModelAdmin):
    list_display = ('id', 'usd_rate', 'eur_rate',)

