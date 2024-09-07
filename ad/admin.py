from django.contrib.admin import ModelAdmin, register, display
from django.utils.safestring import mark_safe

from ad.models import Car, Category, Images, Views, Like, Documents
from modeltranslation.admin import TranslationAdmin

from modeltranslation.admin import TranslationAdmin


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display_links = ("id",)
    list_display = ("id", "name", "parent", "level")
    search_fields = ("name", "parent")


@register(Car)
class CustomUserAdmin(ModelAdmin):
    # list_display_links = ("id",)
    list_display = ("description",)

@register(Images)
class CategoryAdmin(ModelAdmin):
    list_display = ("title",)

@register(Views)
class ViewsAdmin(ModelAdmin):
    list_display = ("profile",)

@register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ('user', 'content_type', 'content_object',)
    list_display_links = ('user',)

@register(Documents)
class DocumentsAdmin(ModelAdmin):
    list_display = ('title', 'profile', 'auto', 'created', 'document_image',)
    list_display_links = ('title',)
    list_filter = ('profile',)
    ordering = ('-created',)

    @display(description='Миниатюра')
    def document_image(self, documents: Documents):
        return mark_safe(f"<img src='{documents.document.url}' width=100>")
