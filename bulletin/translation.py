from modeltranslation.translator import register, TranslationOptions
from users.models import CustomUser


@register(CustomUser)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('username',)