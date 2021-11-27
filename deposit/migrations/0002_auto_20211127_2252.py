# Generated by Django 3.0 on 2021-11-27 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tm_DepositItem',
            fields=[
                ('depositItem_key', models.AutoField(primary_key=True, serialize=False, verbose_name='預金項目ID')),
                ('depositItem_name', models.CharField(max_length=40, verbose_name='預金項目名')),
                ('savings_flag', models.BooleanField(verbose_name='積立項目フラグ')),
                ('order_dsp', models.IntegerField(verbose_name='表示順序')),
                ('delete_flag', models.BooleanField(verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(verbose_name='更新日時')),
                ('deposit_group_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deposititem_deposit_group_key', to='deposit.Tm_DepositGroup', verbose_name='預金項目グループID')),
            ],
            options={
                'verbose_name': '預金項目(Tm_DepositItem)',
                'verbose_name_plural': '預金項目(Tm_DepositItem)',
                'db_table': 'Tm_DepositItem',
                'ordering': ('order_dsp',),
            },
        ),
        migrations.CreateModel(
            name='Tt_Savings',
            fields=[
                ('savings_key', models.AutoField(primary_key=True, serialize=False, verbose_name='貯金設定ID')),
                ('order_dsp', models.IntegerField(verbose_name='表示順序')),
                ('deposit_type', models.IntegerField(verbose_name='貯金タイプ')),
                ('deposit_value', models.IntegerField(verbose_name='金額')),
                ('delete_flag', models.BooleanField(verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(verbose_name='更新日時')),
                ('depositItem_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='savings_deposititem_key', to='deposit.Tm_DepositItem', verbose_name='預金項目ID')),
            ],
            options={
                'verbose_name': '貯金設定(Tt_Savings)',
                'verbose_name_plural': '貯金設定(Tt_Savings)',
                'db_table': 'Tt_Savings',
            },
        ),
        migrations.CreateModel(
            name='Tt_Deposit',
            fields=[
                ('deposit_key', models.AutoField(primary_key=True, serialize=False, verbose_name='預金ID')),
                ('deposit_type', models.IntegerField(verbose_name='貯金タイプ')),
                ('deposit_value', models.IntegerField(verbose_name='金額')),
                ('insert_yyyymmdd', models.CharField(max_length=10, verbose_name='登録年月日')),
                ('delete_flag', models.BooleanField(verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(verbose_name='更新日時')),
                ('memo', models.CharField(max_length=1024, null=True, verbose_name='補足')),
                ('depositItem_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deposit_deposititem_key', to='deposit.Tm_DepositItem', verbose_name='預金項目ID')),
            ],
            options={
                'verbose_name': '預金トラン(Tt_Deposit)',
                'verbose_name_plural': '預金トラン(Tt_Deposit)',
                'db_table': 'Tt_Deposit',
            },
        ),
        migrations.CreateModel(
            name='Tm_MoneyType',
            fields=[
                ('moneyType_key', models.AutoField(primary_key=True, serialize=False, verbose_name='金種ID')),
                ('moneyType_name', models.CharField(max_length=40, verbose_name='金種名')),
                ('delete_flag', models.BooleanField(verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '金種(Tm_MoneyType)',
                'verbose_name_plural': '金種(Tm_MoneyType)',
                'db_table': 'Tm_MoneyType',
                'unique_together': {('moneyType_name',)},
            },
        ),
        migrations.AddField(
            model_name='tm_deposititem',
            name='moneyType_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deposititem_moneytype_key', to='deposit.Tm_MoneyType', verbose_name='金種ID'),
        ),
        migrations.AlterUniqueTogether(
            name='tm_deposititem',
            unique_together={('depositItem_name',)},
        ),
    ]