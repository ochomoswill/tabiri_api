import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from ...models import Country

# Use this to generate Country Model and Country Mapping from its shapefile
# python manage.py ogrinspect tabiri_api/apps/tabiri_gis/data/countries/countries.shp Country --srid=4326 --mapping --multi

# Auto-generated `LayerMapping` dictionary for Country model
country_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'adm0_en': 'ADM0_EN',
    'adm0_pcode': 'ADM0_PCODE',
    'adm0_ref': 'ADM0_REF',
    'adm0alt1en': 'ADM0ALT1EN',
    'adm0alt2en': 'ADM0ALT2EN',
    'date': 'date',
    'validon': 'validOn',
    'validto': 'validTo',
    'geom': 'MULTIPOLYGON',
}


country_shp = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e tabiri_gis
    'data/countries/countries.shp'
)


class Command(BaseCommand):
    help = 'Custom Command to Load Country Shapefile'

    # Load Country Shape File
    def handle(self, *args, **kwargs):
        wc_count = Country.objects.count()
        if wc_count:
            self.stdout.write(self.style.WARNING(
                '{} countries already exist'.format(wc_count)))
            return

        lm = LayerMapping(
            Country,
            country_shp,
            country_mapping,
            transform=False,
            encoding='iso-8859-1'
        )
        lm.save(strict=True, verbose=False)
        self.stdout.write(self.style.SUCCESS("Loaded countries shapefile"))
