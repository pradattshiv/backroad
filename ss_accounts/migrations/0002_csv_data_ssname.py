# Generated by Django 2.2.5 on 2019-11-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ss_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv_data',
            name='SSname',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]