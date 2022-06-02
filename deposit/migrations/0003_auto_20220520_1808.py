# Generated by Django 3.0 on 2022-05-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0002_auto_20220514_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tt_assets',
            name='deposit_key',
        ),
        migrations.AddField(
            model_name='tt_assets',
            name='assets_key',
            field=models.AutoField(default=1, primary_key=True, serialize=False, verbose_name='資産ID'),
            preserve_default=False,
        ),
    ]