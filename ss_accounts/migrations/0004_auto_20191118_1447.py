# Generated by Django 2.2.5 on 2019-11-18 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ss_accounts', '0003_temp_ssdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv_data',
            name='month',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='temp_ssdata',
            name='month',
            field=models.CharField(max_length=30, null=True),
        ),
    ]