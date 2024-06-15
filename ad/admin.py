from django.contrib.admin import ModelAdmin, register

from ad.models import Category
from modeltranslation.admin import TranslationAdmin


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display_links = ("id",)
    list_display = ("id", "name", "parent", "level")
    search_fields = ("name", "parent")
