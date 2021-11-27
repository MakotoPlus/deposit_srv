from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.Tm_DepositGroup)
class AdminTm_Tm_DepositGroup(admin.ModelAdmin):
    fields = ('deposit_group_name', 'order_dsp', 'delete_flag', 'update_date', )
    list_display = ('deposit_group_key', 'deposit_group_name', 'order_dsp', 'delete_flag', 'update_date', )
    ordering = ('deposit_group_key', )
