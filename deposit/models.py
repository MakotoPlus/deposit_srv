from django.contrib.auth import get_user_model
from django.db import models
from deposit.model_base import ModelBase

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
    # u_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='depositgroup_u_user', verbose_name='更新者')
    def __str__(self):
        return self.deposit_group_name
