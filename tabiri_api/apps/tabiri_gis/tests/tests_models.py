from django.contrib.gis.geos import Polygon, MultiPolygon
from django.test import TestCase
from tabiri_api.apps.tabiri_gis.models import Country, County

p1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
p2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
mp = MultiPolygon(p1, p2)


class CountryTest(TestCase):
    """ Test module for Country model """

    def setUp(self):
        Country.objects.create(
            adm0_pcode='UG',
            adm0_en='Uganda',
            shape_leng=0.2345,
            shape_area=0.2345,
            geom=mp
        )
        Country.objects.create(
            adm0_pcode='TZ',
            adm0_en='Tanzania',
            shape_leng=0.5345,
            shape_area=0.5345,
            geom=mp
        )

    def test_country_name(self):
        country_uganda = Country.objects.get(adm0_pcode='UG')
        country_tanzania = Country.objects.get(adm0_pcode='TZ')
        self.assertEqual(
            country_uganda.get_country_name(), "Uganda")
        self.assertEqual(
            country_tanzania.get_country_name(), "Tanzania")


class CountyTest(TestCase):
    """ Test module for County model """

    def setUp(self):
        Country.objects.create(
            adm0_pcode='KE',
            adm0_en='Kenya',
            shape_leng=0.5345,
            shape_area=0.5345,
            geom=mp
        )
        County.objects.create(
            objectid=1,
            county_cod=40,
            county_nam='Kisumu',
            country_code=Country.objects.get(adm0_pcode='KE'),
            shape_leng=0.2345,
            shape_area=0.2345,
            geom=mp
        )
        County.objects.create(
            objectid=2,
            county_cod=1,
            county_nam='Mombasa',
            country_code=Country.objects.get(adm0_pcode='KE'),
            shape_leng=0.2345,
            shape_area=0.2345,
            geom=mp
        )

    def test_county_name(self):
        county_kisumu = County.objects.get(county_cod=40)
        county_mombasa = County.objects.get(county_cod=1)
        self.assertEqual(
            county_kisumu.get_county_name(), "Kisumu")
        self.assertEqual(
            county_mombasa.get_county_name(), "Mombasa")


