from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','display_name', 'email_address']


admin.site.register(Profile,ProfileAdmin)
