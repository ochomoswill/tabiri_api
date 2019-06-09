from django.contrib.gis.geos import MultiPolygon, Polygon
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from tabiri_api.apps.tabiri_gis.models import Country, County
from tabiri_api.apps.tabiri_gis.serializers import CountrySerializer, CountySerializer

p1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
p2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
mp = MultiPolygon(p1, p2)

# initialize the APIClient app
client = Client()


class GetAllCountriesTest(TestCase):
    """ Test module for GET all countries API """

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

    def test_get_all_countries(self):
        # get API response
        response = client.get(reverse('tabiri_gis:countries-list'))
        # get data from db
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllCountiesTest(TestCase):
    """ Test module for GET all counties API """

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

    def test_get_all_counties(self):
        # get API response
        response = client.get(reverse('tabiri_gis:counties-list'))
        # get data from db
        counties = County.objects.all()
        serializer = CountySerializer(counties, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)