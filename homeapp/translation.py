from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(HomeModel)
class HomeModelTranslation(TranslationOptions):
    fields = ('name', 'type', 'home_type', 'description', 'location')


@register(TypeModel)
class TypeTranslation(TranslationOptions):
    fields = ('name',)


@register(LocationModel)
class LocationTranslation(TranslationOptions):
    fields = ('name',)


@register(HomeTypeModel)
class HomeTypeTranslation(TranslationOptions):
    fields = ('name',)
