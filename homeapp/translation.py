from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(HomeModel)
class HomeModelTranslation(TranslationOptions):
    fields = ('description',)


@register(TypeModel)
class TypeTranslation(TranslationOptions):
    fields = ('name',)


@register(HomeTypeModel)
class HomeTypeTranslation(TranslationOptions):
    fields = ('name',)


@register(ComforsTypeModel)
class ComformTranslation(TranslationOptions):
    fields = ('name',)
