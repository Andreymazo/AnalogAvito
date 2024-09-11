from django.contrib.admin import ModelAdmin, register, display
from django.utils.safestring import mark_safe

from ad.models import Car, Category, Images, Views, Like, Documents, MenClothes, MenShoes, WemenShoes, \
    ChildClothesShoes, WemenClothes, BagsKnapsacks
from modeltranslation.admin import TranslationAdmin

from modeltranslation.admin import TranslationAdmin


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display_links = ("id",)
    list_display = ("id", "name", "parent", "level")
    search_fields = ("name", "parent")


@register(Car)
class CarAdmin(ModelAdmin):
    list_display_links = ("id",)
    list_display = ("id", "brand", "description", "archived",)

@register(MenClothes)
class MenClothesAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created', "archived",)

@register(MenShoes)
class MenShoesAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created', "archived",)

@register(WemenClothes)
class WemenClothesShoesAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created', "archived",)

@register(WemenShoes)
class WemenShoesAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created', "archived",)

@register(ChildClothesShoes)
class ChildClothesShoesAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created', "archived",)

@register(BagsKnapsacks)
class BagsKnapsacksAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created', "archived",)

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
