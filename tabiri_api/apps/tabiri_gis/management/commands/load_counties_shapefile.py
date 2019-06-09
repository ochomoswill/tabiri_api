import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from ...models import County

# Use this to generate County Model and County Mapping from its shapefile
# python manage.py ogrinspect tabiri_api/apps/tabiri_gis/data/counties/counties.shp County --srid=4326 --mapping --multi

# Auto-generated `LayerMapping` dictionary for County model
# county_mapping = {
#     'shape_leng': 'Shape_Leng',
#     'shape_area': 'Shape_Area',
#     'adm1_en': 'ADM1_EN',
#     'adm1_pcode': 'ADM1_PCODE',
#     'adm1_ref': 'ADM1_REF',
#     'adm1alt1en': 'ADM1ALT1EN',
#     'adm1alt2en': 'ADM1ALT2EN',
#     'adm0_en': 'ADM0_EN',
#     #'adm0_pcode': 'ADM0_PCODE',
#     'adm0_pcode': {'adm0_pcode': 'ADM0_PCODE'},
#     'date': 'date',
#     'validon': 'validOn',
#     'validto': 'validTo',
#     'geom': 'MULTIPOLYGON',
# }


# Auto-generated `LayerMapping` dictionary for County model
county_mapping = {
    'objectid': 'OBJECTID',
    'id_field': 'ID_',
    'county_nam': 'COUNTY_NAM',
    'const_code': 'CONST_CODE',
    'constituen': 'CONSTITUEN',
    'county_cod': 'COUNTY_COD',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}


county_shp = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e tabiri_gis
    'data/counties/counties.shp'
)


class Command(BaseCommand):
    help = 'Custom Command to Load County Shapefile'

    # Load County Shape File
    def handle(self, *args, **kwargs):
        wc_count = County.objects.count()
        if wc_count:
            self.stdout.write(self.style.WARNING(
                '{} counties already exist'.format(wc_count)))
            return

        lm = LayerMapping(
            County,
            county_shp,
            county_mapping,
            transform=False,
            encoding='iso-8859-1'
        )
        lm.save(strict=True, verbose=False)
        self.stdout.write(self.style.SUCCESS("Loaded counties shapefile"))


