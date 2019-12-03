# Generated by Django 2.2.5 on 2019-11-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ss_accounts', '0002_csv_data_ssname'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp_ssdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SSname', models.CharField(max_length=50)),
                ('Route', models.IntegerField()),
                ('District', models.CharField(max_length=50)),
                ('Town', models.IntegerField()),
                ('Day', models.IntegerField()),
                ('Supervisor', models.CharField(max_length=30)),
                ('VSR', models.CharField(max_length=30)),
                ('Contact', models.IntegerField()),
            ],
        ),
    ]