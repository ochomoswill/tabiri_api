# Generated by Django 2.2.2 on 2019-06-25 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabiri_gis', '0008_auto_20190625_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthfacility',
            name='orgunitid',
            field=models.CharField(max_length=60, primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='VaccineForecastLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('wastage_rate_type', models.CharField(blank=True, max_length=60, null=True)),
                ('mae', models.FloatField(blank=True, null=True)),
                ('mse', models.FloatField(blank=True, null=True)),
                ('rms', models.FloatField(blank=True, null=True)),
                ('orgunitid', models.ForeignKey(db_column='orgunitid', default=37615001008, on_delete=django.db.models.deletion.CASCADE, to='tabiri_gis.HealthFacility')),
            ],
            options={
                'ordering': ['month', 'year'],
            },
        ),
    ]
