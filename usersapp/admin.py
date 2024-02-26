from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['id']
