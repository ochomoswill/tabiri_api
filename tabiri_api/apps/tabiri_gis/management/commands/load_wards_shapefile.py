import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from ...models import Ward

# Use this to generate County Model and County Mapping from its shapefile
# python manage.py ogrinspect tabiri_api/apps/tabiri_gis/data/ward/ward.shp Ward --srid=4326 --mapping --multi

# Auto-generated `LayerMapping` dictionary for Ward model
ward_mapping = {
    'const_code': 'CONST_CODE',
    'shape_area': 'Shape_Area',
    'name': 'NAME',
    'objectid': 'OBJECTID',
    'constituen': 'CONSTITUEN',
    'county_cod': 'COUNTY_COD',
    'shape_leng': 'Shape_Leng',
    'county_nam': 'COUNTY_NAM',
    'shape_le_1': 'Shape_Le_1',
    'geom': 'MULTIPOLYGON',
}


ward_shp = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e tabiri_gis
    'data/ward/ward.shp'
)


class Command(BaseCommand):
    help = 'Custom Command to Load Ward Shapefile'

    # Load Ward Shape File
    def handle(self, *args, **kwargs):
        wc_count = Ward.objects.count()
        if wc_count:
            self.stdout.write(self.style.WARNING(
                '{} wards already exist'.format(wc_count)))
            return

        lm = LayerMapping(
            Ward,
            ward_shp,
            ward_mapping,
            transform=False,
            encoding='iso-8859-1'
        )
        lm.save(strict=True, verbose=False)
        self.stdout.write(self.style.SUCCESS("Loaded wards shapefile"))


