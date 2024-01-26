from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(HomeModel)
class HomeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'rate']
    list_display_links = ['name', 'description', 'rate']


@admin.register(PictureModel)
class PictureModelAdmin(admin.ModelAdmin):
    list_display = ['home', 'pic']
    list_display_links = ['home', 'pic']
