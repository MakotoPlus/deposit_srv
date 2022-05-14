from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.Tm_DepositGroup)
class AdminTm_Tm_DepositGroup(admin.ModelAdmin):
    fields = ('deposit_group_name', 'deposit_flag', 'order_dsp', 'delete_flag', 'update_date', 'u_user', )
    list_display = ('deposit_group_key', 'deposit_group_name', 'deposit_flag', 'order_dsp', 'delete_flag', 'update_date', 'u_user', )
    ordering = ('deposit_group_key', )

@admin.register(models.Tm_DepositItem)
class AdminTm_Tm_DepositItem(admin.ModelAdmin):
    fields = ('depositItem_name', 'deposit_group_key', 'deposit_flag', 'moneyType_key', 'savings_flag', 'order_dsp', 'delete_flag', 'update_date', 'u_user', )
    list_display = ('depositItem_key', 'depositItem_name', 'deposit_group_key', 'deposit_flag', 'moneyType_key', 'savings_flag', 'order_dsp', 'delete_flag', 'update_date', 'u_user', )
    ordering = ('depositItem_key', )

@admin.register(models.Tm_MoneyType)
class AdminTm_Tm_MoneyType(admin.ModelAdmin):
    fields = ('moneyType_name', 'delete_flag', 'update_date', 'u_user', )
    list_display = ('moneyType_key', 'moneyType_name', 'delete_flag', 'update_date', 'u_user', )
    ordering = ('moneyType_key', )

@admin.register(models.Tt_Savings)
class AdminTm_Tt_Savings(admin.ModelAdmin):
    fields = ('depositItem_key', 'deposit_type', 'deposit_value', 'delete_flag', 'update_date', 'u_user', )
    list_display = ('savings_key', 'depositItem_key', 'deposit_type', 'deposit_value', 'delete_flag', 'update_date', 'u_user', )
    ordering = ('savings_key', )

@admin.register(models.Tt_Deposit)
class AdminTm_Tt_Deposit(admin.ModelAdmin):
    fields = ('depositItem_key', 'deposit_type', 'deposit_value', 'insert_yyyymmdd', 'insert_yyyymm', 'delete_flag', 'update_date', 'u_user', 'memo', )
    list_display = ('deposit_key', 'depositItem_key', 'deposit_type', 'deposit_value', 'insert_yyyymmdd', 'insert_yyyymm', 'delete_flag', 'update_date', 'u_user', 'memo', )
    ordering = ('deposit_key', )

@admin.register(models.Tt_Assets)
class AdminTm_Tt_Assets(admin.ModelAdmin):
    fields = ('depositItem_key', 'deposit_type', 'deposit_value', 'insert_yyyymmdd', 'insert_yyyymm', 'delete_flag', 'update_date', 'u_user', 'memo', )
    list_display = ('deposit_key', 'depositItem_key', 'deposit_type', 'deposit_value', 'insert_yyyymmdd', 'insert_yyyymm', 'delete_flag', 'update_date', 'u_user', 'memo', )
    ordering = ('deposit_key', )
