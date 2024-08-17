from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from users.models import CustomUser, OneTimeCode, Profile, Notification
from modeltranslation.admin import TranslationAdmin


# @register(CustomUser)
# class CustomUserAdmin(TranslationAdmin):
#     list_display_links = ("id",)
#     list_display = ("id", "first_name", "last_name", "email")
#     search_fields = ("username", "first_name", "last_name", "email")


@register(OneTimeCode)
class OneTimeCodeAdmin(ModelAdmin):
    list_display_links = ("id", "user",)
    list_display = ("id", "user", "created_at")
    search_fields = ("user",)

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('id', 'email',)
    list_display_links = ('id', 'email',)

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user',)


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user',)