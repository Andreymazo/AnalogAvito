from django.contrib import admin
from django.contrib.admin import ModelAdmin
from personal_account.models import Balance, Payments


@admin.register(Balance)
class BalanceAdmin(ModelAdmin):
    list_display = ('balance', 'currency', 'user',)

@admin.register(Payments)
class Payments(ModelAdmin):
    list_display = ('amount', 'status', 'creating_payment', 'user')
    list_display_links = ('amount',)

