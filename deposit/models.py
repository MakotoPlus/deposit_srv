from django.contrib.auth import get_user_model
from django.db import models
from deposit.model_base import ModelBase
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()
# Create your models here.
#預金項目グループ
class Tm_DepositGroup(ModelBase):
    class Meta:
        db_table = 'Tm_DepositGroup'
        verbose_name = '預金項目グループ(Tm_DepositGroup)'
        verbose_name_plural = '預金項目グループ(Tm_DepositGroup)'
        unique_together = (
            ('deposit_group_name',),
        )
        ordering = ('order_dsp',)

    deposit_group_key = models.AutoField(primary_key=True, verbose_name='預金項目グループID')
    deposit_group_name = models.CharField(max_length=40, verbose_name='預金項目グループ名')
    order_dsp = models.IntegerField(verbose_name='表示順序')
    delete_flag = models.BooleanField(verbose_name='削除フラグ')
    update_date = models.DateTimeField(verbose_name='更新日時')
    u_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='depositgroup_u_user', verbose_name='更新者')
    def __str__(self):
        return self.deposit_group_name

#金種
class Tm_MoneyType(ModelBase):
    class Meta:
        db_table = 'Tm_MoneyType'
        verbose_name = '金種(Tm_MoneyType)'
        verbose_name_plural = '金種(Tm_MoneyType)'
        unique_together = (
            ('moneyType_name',),
        )

    moneyType_key = models.AutoField(primary_key=True, verbose_name='金種ID')
    moneyType_name = models.CharField(max_length=40, verbose_name='金種名')
    delete_flag = models.BooleanField(verbose_name='削除フラグ')
    update_date = models.DateTimeField(verbose_name='更新日時')
    u_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='moneytype_u_user', verbose_name='更新者')
    def __str__(self):
        return self.moneyType_name

#預金項目
class Tm_DepositItem(ModelBase):
    class Meta:
        db_table = 'Tm_DepositItem'
        verbose_name = '預金項目(Tm_DepositItem)'
        verbose_name_plural = '預金項目(Tm_DepositItem)'
        unique_together = (
            ('depositItem_name',),
        )
        ordering = ('order_dsp',)

    depositItem_key = models.AutoField(primary_key=True, verbose_name='預金項目ID')
    depositItem_name = models.CharField(max_length=40, verbose_name='預金項目名')
    deposit_group_key = models.ForeignKey(Tm_DepositGroup, on_delete=models.PROTECT, related_name='deposititem_deposit_group_key', verbose_name='預金項目グループID')
    moneyType_key = models.ForeignKey(Tm_MoneyType, on_delete=models.PROTECT, related_name='deposititem_moneytype_key', verbose_name='金種ID')
    savings_flag = models.BooleanField(verbose_name='積立項目フラグ')
    order_dsp = models.IntegerField(verbose_name='表示順序')
    delete_flag = models.BooleanField(verbose_name='削除フラグ')
    update_date = models.DateTimeField(verbose_name='更新日時')
    u_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deposititem_u_user', verbose_name='更新者')
    def __str__(self):
        return self.depositItem_name


#貯金設定
class Tt_Savings(ModelBase):
    class Meta:
        db_table = 'Tt_Savings'
        verbose_name = '貯金設定(Tt_Savings)'
        verbose_name_plural = '貯金設定(Tt_Savings)'

    savings_key = models.AutoField(primary_key=True, verbose_name='貯金設定ID')
    depositItem_key = models.ForeignKey(Tm_DepositItem, on_delete=models.PROTECT, related_name='savings_deposititem_key', verbose_name='預金項目ID')
    deposit_type = models.IntegerField(verbose_name='貯金タイプ')
    deposit_value = models.IntegerField(verbose_name='金額')
    delete_flag = models.BooleanField(verbose_name='削除フラグ')
    update_date = models.DateTimeField(verbose_name='更新日時')
    u_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='savings_u_user', verbose_name='更新者')

#預金トラン
class Tt_Deposit(ModelBase):
    class Meta:
        db_table = 'Tt_Deposit'
        verbose_name = '預金トラン(Tt_Deposit)'
        verbose_name_plural = '預金トラン(Tt_Deposit)'

    deposit_key = models.AutoField(primary_key=True, verbose_name='預金ID')
    depositItem_key = models.ForeignKey(Tm_DepositItem, on_delete=models.PROTECT, related_name='deposit_deposititem_key', verbose_name='預金項目ID')
    deposit_type = models.IntegerField(verbose_name='貯金タイプ')
    deposit_value = models.IntegerField(verbose_name='金額')
    insert_yyyymmdd = models.CharField(max_length=10, verbose_name='登録年月日')
    insert_yyyymm = models.CharField(max_length=7, verbose_name='登録年月')
    delete_flag = models.BooleanField(verbose_name='削除フラグ')
    update_date = models.DateTimeField(verbose_name='更新日時')
    u_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deposit_u_user', verbose_name='更新者')
    memo = models.CharField(null=True, max_length=1024, verbose_name='補足')
