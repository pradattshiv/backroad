# Generated by Django 2.2.5 on 2019-11-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ss_accounts', '0004_auto_20191118_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csv_data',
            name='month',
            field=models.CharField(blank=True, default=123, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='temp_ssdata',
            name='month',
            field=models.CharField(blank=True, default=123, max_length=30),
            preserve_default=False,
        ),
    ]
