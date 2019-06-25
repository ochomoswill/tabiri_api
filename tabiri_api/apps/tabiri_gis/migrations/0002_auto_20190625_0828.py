# Generated by Django 2.2.2 on 2019-06-25 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabiri_gis', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constituency',
            options={'managed': True, 'verbose_name_plural': 'Constituencies'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'managed': True, 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='county',
            options={'managed': True, 'verbose_name_plural': 'Counties'},
        ),
        migrations.AlterModelOptions(
            name='healthfacility',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='vaccinedemandfeature',
            options={'managed': True, 'ordering': ['month', 'year']},
        ),
        migrations.AlterModelOptions(
            name='ward',
            options={'managed': True},
        ),
    ]
