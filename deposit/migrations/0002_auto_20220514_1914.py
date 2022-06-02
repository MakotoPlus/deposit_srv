# Generated by Django 3.0 on 2022-05-14 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tm_depositgroup',
            name='deposit_flag',
            field=models.BooleanField(default=True, verbose_name='預金データフラグ'),
        ),
        migrations.AddField(
            model_name='tm_deposititem',
            name='deposit_flag',
            field=models.BooleanField(default=True, verbose_name='預金データフラグ'),
        ),
        migrations.CreateModel(
            name='Tt_Assets',
            fields=[
                ('deposit_key', models.AutoField(primary_key=True, serialize=False, verbose_name='預金ID')),
                ('deposit_type', models.IntegerField(verbose_name='貯金タイプ')),
                ('deposit_value', models.IntegerField(verbose_name='金額')),
                ('insert_yyyymmdd', models.CharField(max_length=10, verbose_name='登録年月日')),
                ('insert_yyyymm', models.CharField(max_length=7, verbose_name='登録年月')),
                ('delete_flag', models.BooleanField(verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(verbose_name='更新日時')),
                ('memo', models.CharField(max_length=1024, null=True, verbose_name='補足')),
                ('depositItem_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets_deposititem_key', to='deposit.Tm_DepositItem', verbose_name='預金項目ID')),
                ('u_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assets_u_user', to=settings.AUTH_USER_MODEL, verbose_name='更新者')),
            ],
            options={
                'verbose_name': '資産トラン(Tt_Assets)',
                'verbose_name_plural': '資産トラン(Tt_Assets)',
                'db_table': 'Tt_Assets',
            },
        ),
    ]