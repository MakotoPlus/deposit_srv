from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.Tm_DepositGroup)
class AdminTm_Tm_DepositGroup(admin.ModelAdmin):
    fields = ('deposit_group_name', 'order_dsp', 'delete_flag', 'update_date', )
    list_display = ('deposit_group_key', 'deposit_group_name', 'order_dsp', 'delete_flag', 'update_date', )
    ordering = ('deposit_group_key', )


@admin.register(models.Tm_DepositItem)
class AdminTm_Tm_DepositItem(admin.ModelAdmin):
    fields = ('depositItem_name', 'deposit_group_key', 'moneyType_key', 'savings_flag', 'order_dsp', 'delete_flag', 'update_date',  )
    list_display = ('depositItem_key', 'depositItem_name', 'deposit_group_key', 'moneyType_key', 'savings_flag', 'order_dsp', 'delete_flag', 'update_date',  )
    ordering = ('depositItem_key', )

#@admin.register(models.Tm_MoneyType)
#class AdminTm_Tm_MoneyType(admin.ModelAdmin):
#    fields = ('moneyType_name', 'delete_flag', 'update_date',  )
#    list_display = ('moneyType_key', 'moneyType_name', 'delete_flag', 'update_date',  )
#    ordering = ('moneyType_key', )

@admin.register(models.Tt_Savings)
class AdminTm_Tt_Savings(admin.ModelAdmin):
    fields = ('depositItem_key', 'deposit_type', 'deposit_value', 'delete_flag', 'update_date',  )
    list_display = ('savings_key', 'depositItem_key', 'deposit_type', 'deposit_value', 'delete_flag', 'update_date',  )
    ordering = ('savings_key', )

@admin.register(models.Tt_Deposit)
class AdminTm_Tt_Deposit(admin.ModelAdmin):
    fields = ('depositItem_key', 'deposit_type', 'deposit_value', 'insert_yyyymmdd', 'delete_flag', 'update_date',  'memo', )
    list_display = ('deposit_key', 'depositItem_key', 'deposit_type', 'deposit_value', 'insert_yyyymmdd', 'delete_flag', 'update_date',  'memo', )
    ordering = ('deposit_key', )
