from modeltranslation.translator import register, TranslationOptions
from ad.models import Auto
from users.models import CustomUser


@register(CustomUser)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('email',)

@register(Auto)
class AutoTranslationOption(TranslationOptions):
    fields = ('description',)
