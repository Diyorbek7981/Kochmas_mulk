from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


# Register your models here.

@admin.register(HomeModel)
class HomeModelAdmin(TranslationAdmin):
    list_display = ['name', 'description']
    list_display_links = ['name', 'description']

    # translate u-n
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(PictureModel)
class PictureModelAdmin(admin.ModelAdmin):
    list_display = ['home', 'pic']
    list_display_links = ['home', 'pic']


@admin.register(TypeModel)
class TypeModelAdmin(TranslationAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(HomeTypeModel)
class HomeTypeModelAdmin(TranslationAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(LocationModel)
class LocationModelAdmin(TranslationAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
