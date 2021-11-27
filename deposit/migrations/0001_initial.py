# Generated by Django 3.0 on 2021-11-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tm_DepositGroup',
            fields=[
                ('deposit_group_key', models.AutoField(primary_key=True, serialize=False, verbose_name='預金項目グループID')),
                ('deposit_group_name', models.CharField(max_length=40, verbose_name='預金項目グループ名')),
                ('order_dsp', models.IntegerField(verbose_name='表示順序')),
                ('delete_flag', models.BooleanField(verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(verbose_name='更新日時')),
            ],
            options={
                'verbose_name': '預金項目グループ(Tm_DepositGroup)',
                'verbose_name_plural': '預金項目グループ(Tm_DepositGroup)',
                'db_table': 'Tm_DepositGroup',
                'ordering': ('order_dsp',),
                'unique_together': {('deposit_group_name',)},
            },
        ),
    ]
