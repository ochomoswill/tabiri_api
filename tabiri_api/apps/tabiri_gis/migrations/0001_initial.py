# Generated by Django 2.2.2 on 2019-06-25 08:27

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('objectid', models.BigIntegerField()),
                ('const_code', models.BigIntegerField(db_column='constituency_code', unique=True)),
                ('constituen', models.CharField(db_column='constituency_name', max_length=80)),
                ('county_nam', models.CharField(db_column='county_name', max_length=80)),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Constituencies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('validon', models.DateField(null=True)),
                ('validto', models.DateField(null=True)),
                ('adm0_pcode', models.CharField(db_column='country_code', max_length=50, unique=True)),
                ('adm0_en', models.CharField(db_column='country_name', max_length=50)),
                ('adm0_ref', models.CharField(db_column='country_ref', max_length=50, null=True)),
                ('adm0alt1en', models.CharField(max_length=50, null=True)),
                ('adm0alt2en', models.CharField(max_length=50, null=True)),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('objectid', models.BigIntegerField()),
                ('id_field', models.BigIntegerField(null=True)),
                ('county_cod', models.BigIntegerField(db_column='county_code', unique=True)),
                ('county_nam', models.CharField(db_column='county_name', max_length=80)),
                ('const_code', models.BigIntegerField(db_column='constituency_code', null=True)),
                ('constituen', models.CharField(db_column='constituency_name', max_length=80, null=True)),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Counties',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HealthFacility',
            fields=[
                ('orgunitid', models.CharField(default=37615001008, max_length=60, primary_key=True, serialize=False)),
                ('orgunitname', models.CharField(max_length=200)),
                ('dhis2uid', models.CharField(max_length=60)),
                ('dhis2id', models.IntegerField()),
                ('hierarchylevel', models.IntegerField(blank=True, null=True)),
                ('aggregatedbirths', models.BigIntegerField(blank=True, null=True)),
                ('ward_name', models.CharField(blank=True, max_length=60, null=True)),
                ('ward_dhis2_parent_id', models.IntegerField(blank=True, null=True)),
                ('constituency_name', models.CharField(blank=True, max_length=60, null=True)),
                ('constituency_code', models.IntegerField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'health_facilities',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VaccineDemandFeature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('totalbirths', models.IntegerField(blank=True, null=True)),
                ('totalchildrenvaccinated', models.IntegerField(blank=True, null=True)),
                ('bcg_wastage_rate', models.FloatField(blank=True, null=True)),
                ('tetanus_toxoid_wastage_rate', models.FloatField(blank=True, null=True)),
                ('measles_wastage_rate', models.FloatField(blank=True, null=True)),
                ('opv_wastage_rate', models.FloatField(blank=True, null=True)),
                ('pneumococal_wastage_rate', models.FloatField(blank=True, null=True)),
                ('vit_a_wastage_rate', models.FloatField(blank=True, null=True)),
                ('yellow_fever_wastage_rate', models.FloatField(blank=True, null=True)),
                ('dpt_wastage_rate', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'vaccine_demand_features',
                'ordering': ['month', 'year'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('objectid', models.BigIntegerField(db_column='objectid')),
                ('name', models.CharField(db_column='ward_name', max_length=80)),
                ('constituen', models.CharField(db_column='constituency_name', max_length=80)),
                ('county_cod', models.BigIntegerField(db_column='county_code')),
                ('county_nam', models.CharField(db_column='county_name', max_length=80)),
                ('shape_leng', models.FloatField(db_column='shape_leng')),
                ('shape_area', models.FloatField(db_column='shape_area')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(db_column='geom', null=True, srid=4326)),
                ('ward_dhis2_id', models.BigIntegerField(db_column='ward_dhis2_id', default=37615001008, null=True, unique=True)),
            ],
            options={
                'db_table': 'tabiri_gis_ward',
                'managed': False,
            },
        ),
    ]
