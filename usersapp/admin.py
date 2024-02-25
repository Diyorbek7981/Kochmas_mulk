from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'the_user', 'to_user']
    list_display_links = ['id', 'the_user', 'to_user']
