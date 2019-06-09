import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from ...models import World

world_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'geom': 'MULTIPOLYGON',
}

world_shp = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)  # Folder with this file i.e 'commands'
        )  # Parent of folder where this file is i.e 'management'
    ),  # The application folder itself i.e tabiri_gis
    'data/world/TM_WORLD_BORDERS-0.3.shp'
)

#world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/world/TM_WORLD_BORDERS-0.3.shp'))


class Command(BaseCommand):
    help = 'Custom Command to Load World Shapefile'

    # Load World Shape File
    def handle(self, *args, **kwargs):
        wc_count = World.objects.count()
        if wc_count:
            self.stdout.write(self.style.WARNING(
                '{} countries already exist'.format(wc_count)))
            return

        lm = LayerMapping(
            World,
            world_shp,
            world_mapping,
            transform=False,
            encoding='iso-8859-1'
        )
        lm.save(strict=True, verbose=False)
        self.stdout.write(self.style.SUCCESS("Loaded world shapefile"))

# def load_world_shapefile(verbose=True):
#     lm = LayerMapping(World, world_shp, world_mapping, transform=False, encoding='iso-8859-1')
#     lm.save(strict=True, verbose=verbose)
