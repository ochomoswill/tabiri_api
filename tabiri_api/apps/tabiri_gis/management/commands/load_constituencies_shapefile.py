import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from ...models import Constituency

# Use this to generate Constituency Model and Constituency Mapping from its shapefile
# python manage.py ogrinspect tabiri_api/apps/tabiri_gis/data/constituencies/constituencies.shp Constituency --srid=4326 --mapping --multi

# Auto-generated `LayerMapping` dictionary for SubCounty model
# constituency_mapping = {
#     'shape_leng': 'Shape_Leng',
#     'shape_area': 'Shape_Area',
#     'adm2_en': 'ADM2_EN',
#     'adm2_pcode': 'ADM2_PCODE',
#     'adm2_ref': 'ADM2_REF',
#     'adm2alt1en': 'ADM2ALT1EN',
#     'adm2alt2en': 'ADM2ALT2EN',
#     'adm1_en': 'ADM1_EN',
#     # 'adm1_pcode': 'ADM1_PCODE',
#     'adm1_pcode': {'adm1_pcode': 'ADM1_PCODE'},
#     'adm0_en': 'ADM0_EN',
#     'adm0_pcode': 'ADM0_PCODE',
#     'date': 'date',
#     'validon': 'validOn',
#     'validto': 'ValidTo',
#     'geom': 'MULTIPOLYGON',
# }


# Auto-generated `LayerMapping` dictionary for Constituency model
constituency_mapping = {
    'objectid': 'OBJECTID',
    'county_nam': 'COUNTY_NAM',
    'const_code': 'CONST_CODE',
    'constituen': 'CONSTITUEN',
    'county_cod': 'COUNTY_COD',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}


constituency_shp = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e tabiri_gis
    'data/constituencies/constituencies.shp'
)


class Command(BaseCommand):
    help = 'Custom Command to Load Constituency Shapefile'

    # Load Constituency Shape File
    def handle(self, *args, **kwargs):
        wc_count = Constituency.objects.count()
        if wc_count:
            self.stdout.write(self.style.WARNING(
                '{} constituencies already exist'.format(wc_count)))
            return

        lm = LayerMapping(
            Constituency,
            constituency_shp,
            constituency_mapping,
            transform=False,
            encoding='iso-8859-1'
        )
        lm.save(strict=True, verbose=False)
        self.stdout.write(self.style.SUCCESS("Loaded constituencies shapefile"))


