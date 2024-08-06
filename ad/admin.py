from django.contrib.admin import ModelAdmin, register

from ad.models import Car, Category, Images, Views
from modeltranslation.admin import TranslationAdmin

from modeltranslation.admin import TranslationAdmin


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display_links = ("id",)
    list_display = ("id", "name", "parent", "level")
    search_fields = ("name", "parent")


@register(Car)
class CustomUserAdmin(TranslationAdmin):
    # list_display_links = ("id",)
    list_display = ("description",)

@register(Images)
class CategoryAdmin(ModelAdmin):
    list_display = ("title",)

@register(Views)
class ViewsAdmin(ModelAdmin):
    list_display = ("profile",)