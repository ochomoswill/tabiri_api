# Generated by Django 2.2.2 on 2019-06-25 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabiri_gis', '0004_auto_20190625_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ward',
            name='objectid',
            field=models.BigIntegerField(db_column='objectid', unique=True),
        ),
    ]
