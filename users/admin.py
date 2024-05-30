from django.contrib.admin import ModelAdmin, register

from users.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display_links = ("username",)
    list_display = ("username", "first_name", "last_name", "email")
    search_fields = ("username", "first_name", "last_name", "email")
