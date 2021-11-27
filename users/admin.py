from django.contrib import admin

# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    #fieldsets = (
    #    (None, {'fields': ('username', 'password')}),
    #    (_('Personal info'), {'fields': ('last_name', 'first_name', 'full_name', 'email' )}),
    #    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
    #                                   'groups', 'user_permissions')}),
    #    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    #)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('last_name', 'first_name', 'email' )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'last_name', 'first_name', 'is_staff')
    search_fields = ('username', 'email')
    #filter_horizontal = ('groups', 'user_permissions',)
    