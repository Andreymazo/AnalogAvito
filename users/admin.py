from django.contrib.admin import ModelAdmin, register
from users.models import CustomUser, OneTimeCode
from modeltranslation.admin import TranslationAdmin


@register(CustomUser)
class CustomUserAdmin(TranslationAdmin):
    list_display_links = ("id",)
    list_display = ("id", "first_name", "last_name", "email")
    search_fields = ("username", "first_name", "last_name", "email")


@register(OneTimeCode)
class OneTimeCodeAdmin(ModelAdmin):
    list_display_links = ("id", "user",)
    list_display = ("id", "user", "created_at")
    search_fields = ("user",)


